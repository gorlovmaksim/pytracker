"""Main application factory and entry point for PyTracker.

This module creates and configures the Flask application instance,
initializes extensions, and registers blueprints.
"""

from flask import Flask
from flask_login import LoginManager
from typing import Optional

from config import Config
from db import db
from models import User


def create_app() -> Flask:
    """Create and configure the Flask application.

    Returns:
        Flask: Configured Flask application instance
    """
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    @login_manager.user_loader
    def load_user(user_id: str) -> Optional[User]:
        """Load user by ID for Flask-Login.

        Args:
            user_id (str): String representation of user ID

        Returns:
            Optional[User]: User instance if found, None otherwise
        """
        return db.session.get(User, int(user_id))

    # Register blueprints
    from auth import auth_bp
    from habits import habits_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(habits_bp)

    return app


app = create_app()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
