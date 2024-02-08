""" Unit tests for the queries module. """

import unittest
import uuid
from sqlite3 import IntegrityError

from _types.app import User, QuizIn, QuestionIn, QuizStatus, QuizQuestionAnswerIn
from _types.queries import DatabaseUser
from queries import (
    count_users,
    create_user,
    get_database_user_by_username,
    get_user,
    get_quizzes,
    get_quiz,
    create_update_quiz,
)


class TestQueries(unittest.TestCase):
    """Unit tests for the queries module."""

    def test_get_user(self):
        """Test the get_user function."""

        # Existing user
        user = get_user(1)
        self.assertIsInstance(user, User)
        self.assertEqual(user.id, 1)

        # Non-existing user
        user = get_user(100)
        self.assertIsNone(user)

    def test_create_user_success(self):
        """Test the create_user function with a new user."""

        username = str(uuid.uuid4())[:8]  # Generate a random username
        password = str(uuid.uuid4())[:8]  # Generate a random password
        name = "New User"
        role = "editor"

        user_count = count_users()

        try:
            user_id = create_user(username, password, name, role)
        except IntegrityError:
            user_id = None
        except Exception as e:
            self.fail(e)

        self.assertIsInstance(user_id, int)
        self.assertGreater(user_id, 0)

        self.assertEqual(count_users(), user_count + 1)

        user = get_user(user_id)
        self.assertIsInstance(user, User)
        self.assertEqual(user.id, user_id)

        # Create another user with the same username, expect IntegrityError

        try:
            user_id = create_user(username, password, name, role)
        except IntegrityError:
            user_id = None
        except Exception as e:
            self.fail(e)

        self.assertIsNone(user_id)

        user = get_database_user_by_username(username)
        self.assertIsInstance(user, DatabaseUser)
        self.assertEqual(user.username, username)

    def test_get_quizzes(self):
        """Test the get_quizzes function."""

        # Test case 1: Filter by query and status, expect "General Knowledge" quiz
        query = "General"
        status_list = [QuizStatus.QUIZ_STATUS_PUBLISHED.value]
        limit = 10
        offset = 0

        quizzes, total_count = get_quizzes(query, status_list, limit, offset)

        self.assertEqual(total_count, 1)
        self.assertEqual(len(quizzes), 1)
        self.assertEqual(quizzes[0].name, "General Knowledge")

        # Test case 2: Filter by query and status, expect no quizzes
        query = "Math"
        status_list = [QuizStatus.QUIZ_STATUS_DRAFT.value]
        limit = 10
        offset = 0

        quizzes, total_count = get_quizzes(query, status_list, limit, offset)

        self.assertEqual(total_count, 0)
        self.assertEqual(len(quizzes), 0)

    def test_get_quiz(self):
        """Test the get_quiz function."""

        # Test case 1: Include answers, expect correct answer for the second answer in the first question
        quiz_id = 1
        include_answers = True

        quiz = get_quiz(quiz_id, include_answers)

        self.assertIsNotNone(quiz)
        self.assertEqual(quiz.id, quiz_id)
        self.assertEqual(quiz.name, "General Knowledge")
        self.assertEqual(len(quiz.questions), 10)
        self.assertIsNotNone(quiz.questions[0].answers[1].is_correct)

        # Test case 2: Exclude answers, expect all answer fields to be None
        quiz_id = 1
        include_answers = False

        quiz = get_quiz(quiz_id, include_answers)

        self.assertIsNotNone(quiz)
        self.assertEqual(quiz.id, quiz_id)
        self.assertEqual(quiz.name, "General Knowledge")
        self.assertEqual(len(quiz.questions), 10)
        for question in quiz.questions:
            for answer in question.answers:
                self.assertIsNone(answer.is_correct)

    def test_create_update_quiz(self):
        """Test the create_update_quiz function."""

        # Test case 1: Create a new quiz
        user_id = 1
        quiz_id = None
        quiz = QuizIn(
            name="New Quiz",
            status=QuizStatus.QUIZ_STATUS_PUBLISHED,
            questions=[
                QuestionIn(
                    name="Question 1",
                    answers=[
                        QuizQuestionAnswerIn(name="Answer 1", is_correct=True, order=1),
                        QuizQuestionAnswerIn(
                            name="Answer 2", is_correct=False, order=2
                        ),
                    ],
                    order=1,
                ),
                QuestionIn(
                    name="Question 2",
                    answers=[
                        QuizQuestionAnswerIn(name="Answer 3", is_correct=True, order=1),
                        QuizQuestionAnswerIn(
                            name="Answer 4", is_correct=False, order=2
                        ),
                    ],
                    order=2,
                ),
            ],
        )

        quiz_id = create_update_quiz(user_id, quiz_id, quiz)

        self.assertIsNotNone(quiz_id)
        self.assertIsInstance(quiz_id, int)

        # Validate the created quiz
        created_quiz = get_quiz(quiz_id, include_answers=True)

        self.assertIsNotNone(created_quiz)
        self.assertEqual(created_quiz.id, quiz_id)
        self.assertEqual(created_quiz.name, "New Quiz")
        self.assertEqual(len(created_quiz.questions), 2)

        self.assertEqual(created_quiz.questions[0].name, "Question 1")
        self.assertEqual(created_quiz.questions[0].answers[0].name, "Answer 1")
        self.assertTrue(created_quiz.questions[0].answers[0].is_correct)
        self.assertEqual(created_quiz.questions[0].answers[0].order, 1)
        self.assertEqual(created_quiz.questions[0].answers[1].name, "Answer 2")
        self.assertFalse(created_quiz.questions[0].answers[1].is_correct)
        self.assertEqual(created_quiz.questions[0].answers[1].order, 2)

        self.assertEqual(created_quiz.questions[1].name, "Question 2")
        self.assertEqual(created_quiz.questions[1].answers[0].name, "Answer 3")
        self.assertTrue(created_quiz.questions[1].answers[0].is_correct)
        self.assertEqual(created_quiz.questions[1].answers[0].order, 1)
        self.assertEqual(created_quiz.questions[1].answers[1].name, "Answer 4")
        self.assertFalse(created_quiz.questions[1].answers[1].is_correct)
        self.assertEqual(created_quiz.questions[1].answers[1].order, 2)

        # Test case 2: Update an existing quiz
        quiz = QuizIn(
            name="Updated Quiz",
            status=QuizStatus.QUIZ_STATUS_PUBLISHED,
            questions=[
                QuestionIn(
                    name="Updated Question 1",
                    answers=[
                        QuizQuestionAnswerIn(
                            name="Updated Answer 1", is_correct=True, order=1
                        ),
                        QuizQuestionAnswerIn(
                            name="Updated Answer 2", is_correct=False, order=2
                        ),
                    ],
                    order=1,
                ),
                QuestionIn(
                    name="Updated Question 2",
                    answers=[
                        QuizQuestionAnswerIn(
                            name="Updated Answer 3", is_correct=True, order=1
                        ),
                        QuizQuestionAnswerIn(
                            name="Updated Answer 4", is_correct=False, order=2
                        ),
                    ],
                    order=2,
                ),
            ],
        )

        updated_quiz_id = create_update_quiz(user_id, quiz_id, quiz)

        self.assertEqual(updated_quiz_id, quiz_id)

        # Validate the updated quiz
        updated_quiz = get_quiz(quiz_id, include_answers=True)
        self.assertIsNotNone(updated_quiz)
        self.assertEqual(updated_quiz.name, "Updated Quiz")
        self.assertEqual(len(updated_quiz.questions), 2)

        self.assertEqual(updated_quiz.questions[0].name, "Updated Question 1")
        self.assertEqual(updated_quiz.questions[0].answers[0].name, "Updated Answer 1")
        self.assertTrue(updated_quiz.questions[0].answers[0].is_correct)
        self.assertEqual(updated_quiz.questions[0].answers[0].order, 1)
        self.assertEqual(updated_quiz.questions[0].answers[1].name, "Updated Answer 2")
        self.assertFalse(updated_quiz.questions[0].answers[1].is_correct)
        self.assertEqual(updated_quiz.questions[0].answers[1].order, 2)

        self.assertEqual(updated_quiz.questions[1].name, "Updated Question 2")
        self.assertEqual(updated_quiz.questions[1].answers[0].name, "Updated Answer 3")
        self.assertTrue(updated_quiz.questions[1].answers[0].is_correct)
        self.assertEqual(updated_quiz.questions[1].answers[0].order, 1)
        self.assertEqual(updated_quiz.questions[1].answers[1].name, "Updated Answer 4")
        self.assertFalse(updated_quiz.questions[1].answers[1].is_correct)
        self.assertEqual(updated_quiz.questions[1].answers[1].order, 2)


if __name__ == "__main__":
    unittest.main()
