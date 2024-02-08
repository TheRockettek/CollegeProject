"""This module contains the dataclasses for the database queries."""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class DatabaseUser:
    id: int
    name: str
    username: str
    password: str
    salt: str
    created_at: datetime
    role: str


@dataclass
class DatabaseQuiz:
    id: int
    name: str
    status: str
    created_at: datetime
    updated_at: datetime
    updated_by: int


@dataclass
class DatabaseQuizQuestion:
    id: int
    quiz_id: int
    name: str
    order: int


@dataclass
class DatabaseQuizQuestionAnswer:
    id: int
    question_id: int
    name: str
    order: int
    is_correct: bool
