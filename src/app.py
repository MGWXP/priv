"""
Main application entry point for the Codex Web-Native application.
"""

import os
from flask import Flask, jsonify


def create_app(test_config=None):
    """Create and configure the Flask application."""

    secret_key = os.environ.get("SECRET_KEY")
    if test_config is not None:
        secret_key = test_config.get("SECRET_KEY", secret_key)

    if not secret_key:
        raise RuntimeError("SECRET_KEY must be provided via environment or test config")

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=secret_key,
        DATABASE=os.path.join(app.instance_path, "database.sqlite"),
    )

    if test_config is None:
        # Load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # Load the test config if passed in
        app.config.from_mapping(test_config)

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Register blueprints (will be implemented later)
    # from .api import auth
    # app.register_blueprint(auth.bp)

    @app.route("/")
    def index():
        """Root endpoint to verify the app is running."""
        return jsonify(
            {"status": "success", "message": "Codex Web-Native API is running"}
        )

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
