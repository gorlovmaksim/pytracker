"""
Unit tests for database models.
"""

from datetime import datetime, timezone
from models import Progress


def test_progress_creation(app):
    """Test Progress model creation.

    Args:
        app (Flask): The Flask application instance.
    """
    with app.app_context():
        progress = Progress(
            habit_id=1,
            date=datetime.now(timezone.utc).date(),
            completed=True,
        )
        assert progress.completed is True
