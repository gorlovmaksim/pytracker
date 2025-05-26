"""Unit tests for streak calculators."""

def test_daily_streak_calculator(app):
    """Test daily streak calculation."""
    with app.app_context():
        from models import DailyStreakCalculator, Progress
        from datetime import date, timedelta

        entries = [
            Progress(date=date.today(), completed=True),
            Progress(date=date.today() - timedelta(days=1), completed=True)
        ]
        assert DailyStreakCalculator().calculate(entries) == 2