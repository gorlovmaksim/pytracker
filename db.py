"""Database initialization and configuration."""

from flask_sqlalchemy import SQLAlchemy


# Initialize SQLAlchemy extension
db = SQLAlchemy()


def init_app(app):
    """Initialize database with Flask application.

    Args:
        app: Flask application instance

    Creates all database tables if they don't exist.
    """
    db.init_app(app)
    with app.app_context():
        db.create_all()