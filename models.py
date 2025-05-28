"""Database models for the PyTracker application.

This module defines all database models including:
- User authentication model
- Habit tracking model
- Progress tracking model
- Streak calculation strategies
"""

from datetime import datetime, timedelta, timezone
from typing import List, Set, Optional
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from db import db


class StreakCalculator:
    """Base class for streak calculation strategies.

    This provides the interface for different streak calculation algorithms.
    """

    def calculate(self, progress_entries: List["Progress"]) -> int:
        """Calculate streak based on progress entries.

        Args:
            progress_entries: List of Progress objects

        Returns:
            int: Current streak count

        Raises:
            NotImplementedError: Must be implemented by subclasses
        """
        raise NotImplementedError


class DailyStreakCalculator(StreakCalculator):
    """Calculator for daily streaks.

    Counts consecutive days where the habit was completed.
    """

    def calculate(self, progress_entries: List["Progress"]) -> int:
        """Calculate daily streak.

        Args:
            progress_entries: List of Progress objects sorted by date

        Returns:
            int: Current streak in days
        """
        streak = 0
        # Sort by date in descending order to count from most recent
        for entry in sorted(progress_entries, key=lambda x: x.date, reverse=True):
            if entry.completed:
                streak += 1
            else:
                break
        return streak


class WeeklyStreakCalculator(StreakCalculator):
    """Calculator for weekly streaks.

    Counts number of unique weeks where the habit was completed.
    """

    def calculate(self, progress_entries: List["Progress"]) -> int:
        """Calculate weekly streak.

        Args:
            progress_entries: List of Progress objects

        Returns:
            int: Number of unique weeks with completions
        """
        completed_weeks: Set[int] = set()
        for entry in progress_entries:
            if entry.completed:
                week_num = entry.date.isocalendar()[1]  # Get ISO week number
                completed_weeks.add(week_num)
        return len(completed_weeks)


class User(db.Model, UserMixin):
    """User model for authentication and authorization.

    Attributes:
        id: Primary key
        username: Unique username
        email: Unique email address
        password: Hashed password
        habits: Relationship to user's habits
    """

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    habits = db.relationship("Habit", backref="user", lazy=True)

    def set_password(self, password: str) -> None:
        """Set hashed password for the user.

        Args:
            password: Plain text password to hash and store
        """
        self.password = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """Check if provided password matches the stored hash.

        Args:
            password: Plain text password to verify

        Returns:
            bool: True if password matches, False otherwise
        """
        return check_password_hash(self.password, password)


class Habit(db.Model):
    """Habit model for tracking user habits.

    Attributes:
        id: Primary key
        name: Habit name
        periodicity: Daily or weekly tracking
        target_days: Goal duration in days
        created_at: When the habit was created
        user_id: Foreign key to owning user
        progress: Relationship to progress entries
    """

    __tablename__ = "habit"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    periodicity = db.Column(db.String(20), default="daily")
    target_days = db.Column(db.Integer, default=21)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    progress = db.relationship(
        "Progress", backref="habit", lazy=True, cascade="all, delete-orphan"
    )

    def current_streak(self) -> int:
        """Calculate current streak for the habit.

        Uses appropriate calculator based on periodicity.

        Returns:
            int: Current streak count
        """
        calculator = (
            DailyStreakCalculator()
            if self.periodicity == "daily"
            else WeeklyStreakCalculator()
        )
        return calculator.calculate(self.progress)

    def completion_rate(self) -> int:
        """Calculate completion rate percentage.

        Returns:
            int: Percentage of days completed (0-100)
        """
        completed = len([p for p in self.progress if p.completed])
        total_days = min(
            (datetime.now(timezone.utc).date() - self.created_at.date()).days + 1,
            self.target_days,
        )
        return round((completed / total_days) * 100) if total_days > 0 else 0


class Progress(db.Model):
    """Progress tracking model for habits.

    Attributes:
        id: Primary key
        habit_id: Foreign key to parent habit
        date: Date of progress entry
        completed: Whether habit was completed
    """

    id = db.Column(db.Integer, primary_key=True)
    habit_id = db.Column(db.Integer, db.ForeignKey("habit.id"), nullable=False)
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    completed = db.Column(db.Boolean, default=False)
