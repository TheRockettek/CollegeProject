""" Unit tests for the app module. """

import unittest

from _types.app import QuestionIn, QuizIn, QuizQuestionAnswerIn, QuizStatus
from app import validate_quiz


class TestApp(unittest.TestCase):
    """Unit tests for the app module."""

    # Test that the validate_quiz function returns True and None when the quiz is valid
    def test_validate_quiz_valid(self):
        """Test that the validate_quiz function returns True and None when the quiz is valid."""

        quiz = QuizIn(
            name="Math Quiz",
            status=QuizStatus.QUIZ_STATUS_DRAFT,
            questions=[
                QuestionIn(
                    order=0,
                    name="Question 1",
                    answers=[
                        QuizQuestionAnswerIn(order=0, name="Answer 1", is_correct=True),
                        QuizQuestionAnswerIn(
                            order=0, name="Answer 2", is_correct=False
                        ),
                    ],
                ),
                QuestionIn(
                    order=0,
                    name="Question 2",
                    answers=[
                        QuizQuestionAnswerIn(
                            order=0, name="Answer 3", is_correct=False
                        ),
                        QuizQuestionAnswerIn(order=0, name="Answer 4", is_correct=True),
                    ],
                ),
            ],
        )
        valid, error = validate_quiz(quiz)
        self.assertTrue(valid)
        self.assertIsNone(error)

    # Test that the validation fails when the name is missing
    def test_validate_quiz_missing_name(self):
        """Test that the validation fails when the name is missing."""

        quiz = QuizIn(
            name="",
            status=QuizStatus.QUIZ_STATUS_DRAFT,
            questions=[
                QuestionIn(
                    order=0,
                    name="Question 1",
                    answers=[
                        QuizQuestionAnswerIn(order=0, name="Answer 1", is_correct=True),
                        QuizQuestionAnswerIn(
                            order=0, name="Answer 2", is_correct=False
                        ),
                    ],
                )
            ],
        )
        valid, error = validate_quiz(quiz)
        self.assertFalse(valid)
        self.assertEqual(error, "quiz.name: Missing quiz name")

    # Test that the validation fails when the status is invalid
    def test_validate_quiz_invalid_status(self):
        """Test that the validation fails when the status is invalid."""

        quiz = QuizIn(
            name="Math Quiz",
            status="InvalidStatus",
            questions=[
                QuestionIn(
                    order=0,
                    name="Question 1",
                    answers=[
                        QuizQuestionAnswerIn(order=0, name="Answer 1", is_correct=True),
                        QuizQuestionAnswerIn(
                            order=0, name="Answer 2", is_correct=False
                        ),
                    ],
                )
            ],
        )
        valid, error = validate_quiz(quiz)
        self.assertFalse(valid)
        self.assertEqual(error, "quiz.status: Invalid quiz status 'InvalidStatus'")

    # Test that the validation fails when the questions are missing
    def test_validate_quiz_missing_questions(self):
        """Test that the validation fails when the questions are missing."""

        quiz = QuizIn(
            name="Math Quiz",
            status=QuizStatus.QUIZ_STATUS_DRAFT,
            questions=[],
        )
        valid, error = validate_quiz(quiz)
        self.assertFalse(valid)
        self.assertEqual(error, "quiz.questions: Missing questions")

    # Test that the validation fails when the question name is missing
    def test_validate_quiz_missing_question_name(self):
        """Test that the validation fails when the question name is missing."""

        quiz = QuizIn(
            name="Math Quiz",
            status=QuizStatus.QUIZ_STATUS_DRAFT,
            questions=[
                QuestionIn(
                    order=0,
                    name="",
                    answers=[
                        QuizQuestionAnswerIn(order=0, name="Answer 1", is_correct=True),
                        QuizQuestionAnswerIn(
                            order=0, name="Answer 2", is_correct=False
                        ),
                    ],
                )
            ],
        )
        valid, error = validate_quiz(quiz)
        self.assertFalse(valid)
        self.assertEqual(error, "quiz.questions.0.name: Missing question name")

    # Test that the validation fails when there are no answers
    def test_validate_quiz_missing_answers(self):
        """Test that the validation fails when there are no answers."""

        quiz = QuizIn(
            name="Math Quiz",
            status=QuizStatus.QUIZ_STATUS_DRAFT,
            questions=[
                QuestionIn(
                    order=0,
                    name="Question 1",
                    answers=[],
                )
            ],
        )
        valid, error = validate_quiz(quiz)
        self.assertFalse(valid)
        self.assertEqual(error, "quiz.questions.0.name: Missing answers")

    # Test that the validation fails when the answer name is missing
    def test_validate_quiz_missing_answer_name(self):
        """Test that the validation fails when the answer name is missing."""

        quiz = QuizIn(
            name="Math Quiz",
            status=QuizStatus.QUIZ_STATUS_DRAFT,
            questions=[
                QuestionIn(
                    order=0,
                    name="Question 1",
                    answers=[
                        QuizQuestionAnswerIn(order=0, name="", is_correct=True),
                        QuizQuestionAnswerIn(
                            order=0, name="Answer 2", is_correct=False
                        ),
                    ],
                )
            ],
        )
        valid, error = validate_quiz(quiz)
        self.assertFalse(valid)
        self.assertEqual(
            error,
            "quiz.questions.0.answers.0.name: Missing answer name",
        )

    # Test that the validate_quiz function returns False and the correct error message when the quiz has no correct answer
    def test_validate_quiz_no_correct_answer(self):
        """Test that the validate_quiz function returns False and the correct error message when the quiz has no correct answer."""
        quiz = QuizIn(
            name="Math Quiz",
            status=QuizStatus.QUIZ_STATUS_DRAFT,
            questions=[
                QuestionIn(
                    order=0,
                    name="Question 1",
                    answers=[
                        QuizQuestionAnswerIn(
                            order=0, name="Answer 1", is_correct=False
                        ),
                        QuizQuestionAnswerIn(
                            order=0, name="Answer 2", is_correct=False
                        ),
                    ],
                )
            ],
        )
        valid, error = validate_quiz(quiz)
        self.assertFalse(valid)
        self.assertEqual(
            error,
            "quiz.questions.0.answers: No correct answer set",
        )


if __name__ == "__main__":
    unittest.main()
