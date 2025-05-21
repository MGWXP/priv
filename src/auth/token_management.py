"""JWT token creation and verification utilities."""

from __future__ import annotations

import datetime as _dt
from typing import Any, Dict, Optional

import jwt


def create_token(
    data: Dict[str, Any],
    secret: str,
    expires_delta: Optional[_dt.timedelta] = None,
) -> str:
    """Create a JWT token from ``data`` signed with ``secret``.

    Args:
        data: Payload to include in the token.
        secret: Secret key used to sign the token.
        expires_delta: Optional expiration delta to include in the payload.

    Returns:
        Encoded JWT token as a string.
    """

    payload = data.copy()
    if expires_delta:
        payload["exp"] = _dt.datetime.utcnow() + expires_delta
    return jwt.encode(payload, secret, algorithm="HS256")


def verify_token(token: str, secret: str) -> Dict[str, Any]:
    """Verify a JWT ``token`` and return its payload.

    Args:
        token: Encoded JWT token string.
        secret: Secret key expected to have signed the token.

    Returns:
        The decoded token payload.

    Raises:
        jwt.PyJWTError: If the token is invalid or expired.
    """

    return jwt.decode(token, secret, algorithms=["HS256"])
