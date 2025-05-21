"""Entry point for the src package with a minimal Flask app."""

from flask import Flask

app = Flask(__name__)


@app.route("/")
def index():
    """Basic index route."""
    return {"status": "ok"}


if __name__ == "__main__":
    app.run()
