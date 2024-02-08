"""This module contains functions for querying the database."""

import sqlite3
from datetime import datetime
from typing import List, Optional

import utilities
from _types.app import (
    Question,
    Quiz,
    QuizIn,
    QuizQuestionAnswer,
    QuizStatus,
    QuizWithQuestionCount,
    User,
    UserRole,
)
from _types.queries import DatabaseUser

# Specify the path to your SQLite database file
DATABASE_PATH = "database.db"

# Connect to the database
conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)

# User Management


def get_database_user_by_username(username: str) -> Optional[DatabaseUser]:
    """Get user from the database using the provided username."""

    cursor = conn.cursor()
    cursor.execute(
        "SELECT `id`, `name`, `username`, `password`, `salt`, `created_at`, `role` FROM user WHERE username = ?",
        (username,),
    )
    row = cursor.fetchone()
    cursor.close()

    if row is None:
        return None

    return DatabaseUser(
        row[0], row[1], row[2], row[3], row[4], utilities.convert_from_iso(row[5]), row[6]
    )


def get_user(user_id: int) -> Optional[User]:
    """Get user from the database using the provided ID."""
    cursor = conn.cursor()
    cursor.execute(
        "SELECT `id`, `name`, `username`, `created_at`, `role` FROM user WHERE id = ?",
        (user_id,),
    )
    row = cursor.fetchone()
    cursor.close()

    if row is None:
        return None

    return User(row[0], row[1], row[2], utilities.convert_from_iso(row[3]), row[4])


def create_user(username: str, plain_password: str, name: str, role: str) -> int:
    """Create a new user in the database. Handles generating a salt and hashing the password."""

    # Generate salt cryptographically
    salt = utilities.generate_salt()

    # Hash the password with the salt
    hashed_password = utilities.hash_password(plain_password, salt)

    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO user (name, username, password, salt, created_at, role) VALUES (?, ?, ?, ?, ?, ?)",
        (name, username, hashed_password, salt, datetime.now().isoformat(), role),
    )
    cursor.close()
    conn.commit()

    return cursor.lastrowid


def count_users() -> int:
    """Count the number of users in the database."""

    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM user")
    count = cursor.fetchone()[0]
    cursor.close()

    return count


# Quiz Management


def get_quizzes(
    query: str, status_list: list[str], limit: int, offset: 0
) -> [list[QuizWithQuestionCount], int]:
    """Get quizzes from the database. Handles filtering by query and status, and paginating the results."""

    # Query quizzes
    cursor = conn.cursor()
    cursor.execute(
        f"""
            SELECT
                quiz.id,
                quiz.name,
                quiz.status,
                quiz.created_at,
                quiz.updated_at,
                (SELECT COUNT(*) FROM quiz_question WHERE quiz_question.quiz_id = quiz.id) AS question_count,
                quiz.updated_by,
                user.name AS user_name,
                user.username AS user_username,
                user.created_at AS user_created_at,
                user.role AS user_role
            FROM
                quiz
                LEFT JOIN user ON user.id = quiz.updated_by
            WHERE
                (quiz.name LIKE ? OR ? = '')
                AND quiz.status in {utilities.build_list(len(status_list))}
            LIMIT ? OFFSET ?
        """,
        (
            "%" + query + "%",
            query,
            *status_list,
            limit,
            offset,
        ),
    )
    rows = cursor.fetchall()
    cursor.close()

    if rows:
        results = [
            QuizWithQuestionCount(
                id=row[0],
                name=row[1],
                status=QuizStatus(row[2]),
                questions=None,
                created_at=utilities.convert_from_iso(row[3]),
                updated_at=utilities.convert_from_iso(row[4]),
                question_count=row[5],
                updated_by=User(
                    id=row[6],
                    name=row[7],
                    username=row[8],
                    created_at=utilities.convert_from_iso(row[9]),
                    role=UserRole(row[10]),
                ),
            )
            for row in rows
        ]
    else:
        results = []

    # Get the total count of quizzes
    cursor = conn.cursor()
    cursor.execute(
        f"""
            SELECT
                COUNT(*)
            FROM
                quiz
            WHERE
                (quiz.name LIKE ? OR ? = '')
                AND quiz.status in {utilities.build_list(len(status_list))}
        """,
        (
            "%" + query + "%",
            query,
            *status_list,
        ),
    )
    rows = cursor.fetchone()
    count = rows[0] if rows else 0
    cursor.close()

    return results, count


def get_quiz(quiz_id: int, include_answers: bool) -> Optional[Quiz]:
    """Get a quiz from the database using the provided ID."""

    cursor = conn.cursor()
    cursor.execute(
        """
            SELECT
                quiz.id,
                quiz.name,
                quiz.status,
                quiz.created_at,
                quiz.updated_at,
                quiz.updated_by,
                user.name AS user_name,
                user.username AS user_username,
                user.created_at AS user_created_at,
                user.role AS user_role,
                quiz_question.id AS quiz_question_id,
                quiz_question.name AS quiz_question_name,
                quiz_question.`order` AS quiz_question_order,
                quiz_question_answer.id AS quiz_question_answer_id,
                quiz_question_answer.name AS quiz_question_answer,
                quiz_question_answer.`order` AS quiz_question_answer_order,
                quiz_question_answer.is_correct AS quiz_question_answer_is_correct
            FROM
                quiz
                LEFT JOIN user ON user.id = quiz.updated_by
                JOIN quiz_question ON quiz_question.quiz_id = quiz.id
                JOIN quiz_question_answer ON quiz_question_answer.question_id = quiz_question.id
            WHERE
                quiz.id = ?
            ORDER BY quiz_question_order, quiz_question_answer_order
        """,
        (quiz_id,),
    )
    rows = cursor.fetchall()
    cursor.close()

    if len(rows) == 0:
        return None

    first_row = rows[0]
    quiz = Quiz(
        name=first_row[1],
        status=QuizStatus(first_row[2]),
        questions=extract_questions(rows, include_answers),
        created_at=utilities.convert_from_iso(first_row[3]),
        updated_at=utilities.convert_from_iso(first_row[4]),
        updated_by=User(
            id=first_row[5],
            name=first_row[6],
            username=first_row[7],
            created_at=utilities.convert_from_iso(first_row[8]),
            role=UserRole(first_row[9]),
        ),
        id=first_row[0],
    )

    return quiz


def extract_questions(rows, include_answers: bool) -> List[Question]:
    """Extract questions from the provided rows."""

    questions = {}

    for row in rows:
        question_id = row[10]

        if question_id not in questions:
            questions[question_id] = Question(
                name=row[11],
                order=row[12],
                id=question_id,
                answers=[],
                quiz_id=row[0]
            )

        questions[question_id].answers.append(
            QuizQuestionAnswer(
                name=row[14],
                order=row[15],
                is_correct=bool(row[16]) if include_answers else None,
                id=row[13],
                question_id=question_id,
            )
        )

        # Sort answers by order
        questions[question_id].answers.sort(key=lambda x: x.order)

    values = list(questions.values())
    values.sort(key=lambda x: x.order)

    return values


def create_update_quiz(user_id: int, quiz_id: int, quiz: QuizIn) -> int:
    """Create a new quiz in the database."""

    try:
        cursor = conn.cursor()

        if quiz_id:
            cursor.execute(
                "DELETE FROM quiz_question_answer WHERE question_id IN (SELECT id FROM quiz_question WHERE quiz_id = ?);",
                (quiz_id,),
            )
            cursor.execute("DELETE FROM quiz_question WHERE quiz_id = ?;", (quiz_id,))

        cursor.execute(
            """
                INSERT INTO
                    quiz (id, name, status, created_at, updated_at, updated_by)
                VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT(id) DO UPDATE SET
                    name=excluded.name,
                    status=excluded.status,
                    updated_at=excluded.updated_at,
                    updated_by=excluded.updated_by;
            """,
            (
                quiz_id or None,
                quiz.name,
                quiz.status.value,
                datetime.now().isoformat(),
                datetime.now().isoformat(),
                user_id,
            ),
        )

        if not quiz_id:
            quiz_id = cursor.lastrowid

        for question in quiz.questions:
            cursor.execute(
                "INSERT INTO quiz_question (name, `order`, quiz_id) VALUES (?, ?, ?)",
                (question.name, question.order, quiz_id),
            )
            question_id = cursor.lastrowid

            for answer in question.answers:
                cursor.execute(
                    "INSERT INTO quiz_question_answer (name, `order`, is_correct, question_id) VALUES (?, ?, ?, ?)",
                    (answer.name, answer.order, answer.is_correct, question_id),
                )

        cursor.close()
    except Exception as e:
        conn.rollback()
        raise e
    else:
        conn.commit()

    return quiz_id


# Bootstrap tables
with open("schema.sql", "r", encoding="utf-8") as file:
    conn.executescript(file.read())
