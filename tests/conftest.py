"""
Configuration and fixtures for pytest.
"""

import pytest
from app import create_app
from db import db as _db


@pytest.fixture
def app():
    """Create and configure a test Flask application.

    Yields:
        Flask: Configured Flask application for testing.
    """
    app = create_app()
    app.config.update(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "WTF_CSRF_ENABLED": False,
        }
    )

    with app.app_context():
        _db.create_all()
        yield app
        _db.session.remove()
        _db.drop_all()


@pytest.fixture
def client(app):
    """Create a test client for the Flask application.

    Args:
        app (Flask): The Flask application instance.

    Returns:
        FlaskClient: A test client for the Flask app.
    """
    return app.test_client()


@pytest.fixture
def test_user(app):
    """Create a test user for authentication tests.

    Args:
        app (Flask): The Flask application instance.

    Returns:
        User: The created test user.
    """
    with app.app_context():
        from models import User
        from werkzeug.security import generate_password_hash

        user = User(
            username="testuser",
            email="test@example.com",
            password=generate_password_hash("Test1234!"),
        )
        _db.session.add(user)
        _db.session.commit()
        return user
