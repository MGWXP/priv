"""Utilities for hashing and verifying passwords."""

from __future__ import annotations

import bcrypt


def hash_password(password: str) -> str:
    """Hash a plaintext password using bcrypt.

    Args:
        password: The plaintext password to hash.

    Returns:
        The bcrypt hash of the password encoded as a UTF-8 string.
    """

    password_bytes = password.encode("utf-8")
    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    return hashed.decode("utf-8")


def verify_password(password: str, password_hash: str) -> bool:
    """Verify a plaintext password against a bcrypt hash.

    Args:
        password: The plaintext password to check.
        password_hash: The stored bcrypt hash.

    Returns:
        ``True`` if the password matches the hash, ``False`` otherwise.
    """

    password_bytes = password.encode("utf-8")
    hash_bytes = password_hash.encode("utf-8")
    return bcrypt.checkpw(password_bytes, hash_bytes)
