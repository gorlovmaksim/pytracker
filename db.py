"""
Database initialization and configuration.
"""

from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy extension
db = SQLAlchemy()


def init_app(app):
    """Initialize the database with the Flask application.

    Args:
        app (Flask): The Flask application instance.
    """
    db.init_app(app)
    with app.app_context():
        db.create_all()
