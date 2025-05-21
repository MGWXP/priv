import pytest
from datetime import timedelta

from src.auth import (
    hash_password,
    verify_password,
    User,
    create_token,
    verify_token,
)


def test_password_hashing_and_verification():
    password = "secret"
    hashed = hash_password(password)
    assert hashed != password
    assert verify_password(password, hashed) is True
    assert verify_password("wrong", hashed) is False


def test_user_password_methods():
    user = User(username="alice", email="alice@example.com")
    user.set_password("mypassword")
    assert user.check_password("mypassword") is True
    assert user.check_password("other") is False


def test_token_creation_and_verification():
    data = {"user_id": 1}
    token = create_token(data, "secret", expires_delta=timedelta(seconds=2))
    payload = verify_token(token, "secret")
    assert payload["user_id"] == 1

    # expired token should raise exception
    expired_token = create_token(data, "secret", expires_delta=timedelta(seconds=-1))
    with pytest.raises(Exception):
        verify_token(expired_token, "secret")
