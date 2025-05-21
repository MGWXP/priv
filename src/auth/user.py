"""Simple user model and authentication helpers."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from .password import hash_password, verify_password


@dataclass
class User:
    """Representation of an application user."""

    username: str
    email: Optional[str] = None
    password_hash: Optional[str] = field(default=None, repr=False)

    def set_password(self, password: str) -> None:
        """Hash and store the user's password."""

        self.password_hash = hash_password(password)

    def check_password(self, password: str) -> bool:
        """Return ``True`` if ``password`` matches the stored hash."""

        if self.password_hash is None:
            return False
        return verify_password(password, self.password_hash)
