"""The main application file for the backend. This file contains the API routes and the main application logic."""

import logging
import os
from dataclasses import dataclass
from functools import wraps
from http import HTTPStatus
from secrets import token_urlsafe
from typing import Any, Callable, Optional

import queries
import utilities
from _types.app import Quiz, QuizIn, QuizStatus, QuizWithQuestionCount, User, UserRole
from dotenv import load_dotenv
from quart import (
    Quart,
    abort,
    current_app,
    redirect,
    request,
    session,
    send_from_directory,
)
from quart_schema import QuartSchema, validate_request, validate_response

app = Quart(__name__)
QuartSchema(app)

# Load SECRET_KEY from environment variables or generate a random value.

load_dotenv()

secret_key = os.environ.get("SECRET_KEY")
if not secret_key:
    logging.warning(
        "No SECRET_KEY set in .env file, using a random value. This will not persist across server restarts."
    )
    secret_key = token_urlsafe(32)

app.config["SECRET_KEY"] = secret_key
app.static_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dist")

# Setup the routes for the API.


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
async def serve_spa(path: str):
    """Serve the single page application."""

    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        # Serve the requested file from the static folder
        return await send_from_directory(app.static_folder, path)

    # Serve the index.html file for all other routes
    return await send_from_directory(app.static_folder, "index.html")


def valid_login_required(func) -> Callable:
    """Decorator to require a valid login for a route."""

    @wraps(func)
    async def wrapper(*args: Any, **kwargs: Any) -> Any:
        if "user_id" not in session:
            return abort(HTTPStatus.UNAUTHORIZED)

        user: User = queries.get_user(session["user_id"])
        if user is None:
            return abort(HTTPStatus.UNAUTHORIZED)

        session["user"] = user

        return await current_app.ensure_async(func)(*args, **kwargs)

    return wrapper


@dataclass
class LoginForm:
    """Form for logging in."""

    username: str
    password: str
    remember: bool


# POST /api/auth/login
@app.post("/api/auth/login")
@validate_request(LoginForm)
@validate_response(User)
async def post_login(data: LoginForm) -> Optional[User]:
    """Log the user in."""

    database_user = queries.get_database_user_by_username(data.username)
    if database_user is None:
        logging.error("User '%s' not found", data.username)
        abort(HTTPStatus.UNAUTHORIZED, "Invalid username or password")

    if not utilities.compare_passwords(
        data.password, database_user.password, database_user.salt
    ):
        logging.error("Invalid password for user '%s'", database_user.username)
        abort(HTTPStatus.UNAUTHORIZED, "Invalid username or password")

    # Create a User object from the DatabaseUser
    user = User(
        id=database_user.id,
        name=database_user.name,
        username=database_user.username,
        created_at=database_user.created_at,
        role=database_user.role,
    )

    session.permanent = data.remember
    session["user_id"] = user.id
    session["user"] = user

    return user


# GET /logout
@app.get("/logout")
async def logout() -> None:
    """Log the user out."""

    session.clear()
    return redirect("/login")


# GET /api/users/@me
@app.get("/api/users/@me")
@valid_login_required
@validate_response(User)
async def get_logged_in_user() -> Optional[User]:
    """Get the currently logged in user."""

    return session["user"]


@dataclass
class Quizzes:
    """Response for the /api/quizzes route."""

    quizzes: list[QuizWithQuestionCount]
    count: int


# GET /api/quizzes
@app.get("/api/quizzes")
@valid_login_required
@validate_response(Quizzes)
async def get_quizzes() -> Optional[Quizzes]:
    """Returns a list of quizzes. If the user is an editor, include draft quizzes."""

    query = ""
    limit = 10
    offset = 0
    status = None

    try:
        query = request.args.get("query", query).strip()
        limit = int(request.args.get("limit", limit))
        offset = int(request.args.get("offset", offset))

        _status = request.args.get("status", None)
        if _status:
            status = QuizStatus(_status)
    except Exception as e:
        print(e)

    # Sanitize and validate the query parameters.
    query = query.strip()
    limit = max(1, min(limit, 100))
    offset = max(0, offset)

    # Validate the passed status.
    status_filter: list[QuizStatus] = []
    if status is None:
        # If a status is not provided (such as selecting ALL), default to published for regular users and published and draft for editors.
        if UserRole(session["user"].role) == UserRole.USER_ROLE_EDITOR:
            status_filter = [
                QuizStatus.QUIZ_STATUS_PUBLISHED,
                QuizStatus.QUIZ_STATUS_DRAFT,
            ]
        else:
            status_filter = [QuizStatus.QUIZ_STATUS_PUBLISHED]
    else:
        # If a status is provided, ensure it is a valid status for the user's role.
        if (
            status == QuizStatus.QUIZ_STATUS_PUBLISHED
            or UserRole(session["user"].role) == UserRole.USER_ROLE_EDITOR
        ):
            status_filter = [status]
        else:
            # If the user is not an editor, they can only view published quizzes.
            return abort(HTTPStatus.BAD_REQUEST)

    quizzes, count = queries.get_quizzes(
        query, [e.value for e in status_filter], limit, offset
    )
    return Quizzes(quizzes=quizzes, count=count)


# GET /api/quizzes/:quiz_id
@app.get("/api/quizzes/<int:quiz_id>")
@valid_login_required
@validate_response(Quiz)
async def get_quiz(quiz_id: int) -> Optional[Quiz]:
    """Get a single quiz by ID. If the user is an editor or viewer, include the answers."""

    return queries.get_quiz(
        quiz_id,
        include_answers=UserRole(session["user"].role)
        in [UserRole.USER_ROLE_EDITOR, UserRole.USER_ROLE_VIEWER],
    )


# POST /api/quizzes
@app.post("/api/quizzes")
@valid_login_required
@validate_request(QuizIn)
@validate_response(Quiz)
async def post_quiz(data: QuizIn) -> Optional[Quiz]:
    """Create a new quiz. Requires UserRoleEditor."""
    if UserRole(session["user"].role) != UserRole.USER_ROLE_EDITOR:
        return abort(HTTPStatus.FORBIDDEN)

    is_valid, validation_message = validate_quiz(data)
    if not is_valid:
        return abort(HTTPStatus.BAD_REQUEST, validation_message)

    return queries.get_quiz(
        queries.create_update_quiz(session["user_id"], None, data), include_answers=True
    )


# PUT /api/quizzes/:quiz_id
@app.put("/api/quizzes/<int:quiz_id>")
@valid_login_required
@validate_request(QuizIn)
@validate_response(Quiz)
async def put_quiz(quiz_id: int, data: QuizIn) -> Optional[Quiz]:
    """Update an existing quiz. Requires UserRoleEditor."""

    if UserRole(session["user"].role) != UserRole.USER_ROLE_EDITOR:
        return abort(HTTPStatus.FORBIDDEN)

    is_valid, validation_message = validate_quiz(data)
    if not is_valid:
        return abort(HTTPStatus.BAD_REQUEST, validation_message)

    return queries.get_quiz(
        queries.create_update_quiz(session["user_id"], quiz_id, data),
        include_answers=True,
    )


# DELETE /api/quizzes/:id
@app.delete("/api/quizzes/<int:quiz_id>")
@valid_login_required
async def delete_quiz(quiz_id: int) -> None:
    """Delete a quiz. Requires UserRoleEditor."""

    if UserRole(session["user"].role) != UserRole.USER_ROLE_EDITOR:
        return abort(HTTPStatus.FORBIDDEN)

    quiz = queries.get_quiz(quiz_id, include_answers=True)
    if quiz is None:
        return abort(HTTPStatus.NOT_FOUND)

    quiz.status = QuizStatus.QUIZ_STATUS_ARCHIVED

    queries.create_update_quiz(session["user_id"], quiz_id, quiz)

    return "", HTTPStatus.OK


def validate_quiz(quiz: QuizIn):
    """Validate a quiz."""

    if not quiz.name:
        return False, "quiz.name: Missing quiz name"

    if not quiz.status or quiz.status not in [
        QuizStatus.QUIZ_STATUS_DRAFT,
        QuizStatus.QUIZ_STATUS_PUBLISHED,
        QuizStatus.QUIZ_STATUS_ARCHIVED,
    ]:
        return False, "quiz.status: Invalid quiz status '" + quiz.status + "'"

    if not quiz.questions or len(quiz.questions) < 1:
        return False, "quiz.questions: Missing questions"

    for question_index, question in enumerate(quiz.questions):
        if not question.name:
            return False, f"quiz.questions.{question_index}.name: Missing question name"

        if not question.answers or len(question.answers) < 1:
            return False, f"quiz.questions.{question_index}.name: Missing answers"

        has_correct_answer = False
        for answer_index, answer in enumerate(question.answers):
            if not answer.name:
                return (
                    False,
                    f"quiz.questions.{question_index}.answers.{answer_index}.name: Missing answer name",
                )

            if answer.is_correct:
                has_correct_answer = True

        if not has_correct_answer:
            return (
                False,
                f"quiz.questions.{question_index}.answers: No correct answer set",
            )

    return True, None


if __name__ == "__main__":
    # Check if there are any users in the user table. If not, prompt the user to create a user.
    if queries.count_users() == 0:
        print(
            "No users found in the user table. Please run create_user.py to create a user"
        )

    app.run(debug=os.environ.get("DEBUG", False))
