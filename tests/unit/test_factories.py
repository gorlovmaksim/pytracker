"""
Unit tests for factory classes.
"""


def test_habit_factory(app):
    """Test HabitFactory creation.

    Args:
        app (Flask): The Flask application instance.
    """
    with app.app_context():
        from habits.factory import HabitFactory
        from models import Habit

        habit = HabitFactory.create(
            name="Test", periodicity="daily", user_id=1, target_days=21
        )
        assert isinstance(habit, Habit)
        assert habit.name == "Test"
