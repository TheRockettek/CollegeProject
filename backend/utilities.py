""" This module contains utility functions for the backend. """

from datetime import datetime
from hashlib import sha256
from hmac import compare_digest
from secrets import token_hex


def hash_password(password: str, salt: str) -> str:
    """Hash the provided password using the provided salt."""

    combined = password + salt

    # Hash the combined string using SHA-256
    hashed_password = sha256(combined.encode()).hexdigest()

    return hashed_password


def compare_passwords(password: str, hashed_password: str, salt: str) -> bool:
    """Compare the provided password with the hashed password using the provided salt."""

    # Hash the provided password with the same salt
    new_hashed_password = hash_password(password, salt)

    # Use a constant-time comparison function to compare the two hashed passwords
    return compare_digest(hashed_password, new_hashed_password)


def generate_salt() -> str:
    """Generate a random 16-byte salt using secrets module."""

    salt = token_hex(16)

    return salt


def convert_from_iso(iso_date) -> datetime | None:
    """Convert ISO 8601 date string to datetime object. Return None if conversion fails."""

    try:
        return datetime.fromisoformat(iso_date)
    except ValueError:
        return None


def build_list(length) -> str:
    """Build a string of question marks for use in SQL queries."""
    return "(" + ", ".join(["?" for _ in range(length)]) + ")"
