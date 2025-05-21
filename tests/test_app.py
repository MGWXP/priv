import os
from flask import Flask
from src.app import create_app


def test_create_app_returns_flask_app():
    """Verify that create_app returns a configured Flask instance."""

    app = create_app({"TESTING": True})
    assert isinstance(app, Flask)
    assert app.config["TESTING"] is True
    assert app.config["SECRET_KEY"] == os.environ.get("SECRET_KEY")


def test_index_route_returns_success():
    """Ensure the index route responds with the expected payload."""

    app = create_app({"TESTING": True})
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200
    assert response.get_json() == {
        "status": "success",
        "message": "Codex Web-Native API is running",
    }
