"""Main application factory for PyTracker."""

from flask import Flask
from flask_login import LoginManager

from config import Config
from db import db
from models import User


def create_app():
    """Create and configure the Flask application.

    Returns:
        Flask: The configured Flask application instance
    """
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(user_id):
        """Load user by ID for Flask-Login.

        Args:
            user_id: ID of the user to load

        Returns:
            User: User instance or None if not found
        """
        return User.query.get(int(user_id))

    # Register blueprints
    from auth import auth_bp
    from habits import habits_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(habits_bp)

    return app


if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True)