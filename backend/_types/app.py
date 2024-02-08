"""This module contains the dataclasses and enumerators used in the application."""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum

# Define enumerators for the user roles and quiz status.


class UserRole(Enum):
    """User roles enumeration."""

    USER_ROLE_EDITOR = "editor"
    USER_ROLE_VIEWER = "viewer"
    USER_ROLE_RESTRICTED = "restricted"


class QuizStatus(Enum):
    """Quiz status enumeration."""

    QUIZ_STATUS_DRAFT = "draft"
    QUIZ_STATUS_PUBLISHED = "published"
    QUIZ_STATUS_ARCHIVED = "archived"


# Setup classes based on the database schema.
# QuizQuestionAnswer -> QuizQuestion -> Quiz


@dataclass
class User:
    id: int
    name: str
    username: str
    created_at: datetime
    role: UserRole


@dataclass
class QuizQuestionAnswerIn:
    name: str
    order: int
    is_correct: bool


@dataclass
class QuizQuestionAnswer(QuizQuestionAnswerIn):
    id: int
    question_id: int


@dataclass
class QuestionIn:
    name: str
    order: int
    answers: list[QuizQuestionAnswerIn]


@dataclass
class Question(QuestionIn):
    id: int
    quiz_id: int


@dataclass
class QuizIn:
    name: str
    status: QuizStatus
    questions: list[QuestionIn] | None


@dataclass
class Quiz(QuizIn):
    id: int
    updated_by: User | None
    created_at: datetime
    updated_at: datetime


@dataclass
class QuizWithQuestionCount(Quiz):
    question_count: int
