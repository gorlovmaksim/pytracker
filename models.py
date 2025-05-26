"""Database models for the application."""

from datetime import datetime, timedelta, timezone
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from db import db


class StreakCalculator:
    """Base class for streak calculation strategies."""

    def calculate(self, progress_entries):
        """Calculate streak based on progress entries."""
        raise NotImplementedError


class DailyStreakCalculator(StreakCalculator):
    """Calculator for daily streaks."""

    def calculate(self, progress_entries):
        """Calculate daily streak."""
        streak = 0
        for entry in sorted(progress_entries, key=lambda x: x.date, reverse=True):
            if entry.completed:
                streak += 1
            else:
                break
        return streak


class WeeklyStreakCalculator(StreakCalculator):
    """Calculator for weekly streaks."""

    def calculate(self, progress_entries):
        """Calculate weekly streak."""
        completed_weeks = set()
        for entry in progress_entries:
            if entry.completed:
                week_num = entry.date.isocalendar()[1]
                completed_weeks.add(week_num)
        return len(completed_weeks)


class User(db.Model, UserMixin):
    """User model for authentication."""

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    habits = db.relationship('Habit', backref='user', lazy=True)

    def set_password(self, password):
        """Set hashed password for the user."""
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """Check if provided password matches the stored hash."""
        return check_password_hash(self.password, password)


class Habit(db.Model):
    """Habit model for tracking user habits."""

    __tablename__ = 'habit'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    periodicity = db.Column(db.String(20), default='daily')
    target_days = db.Column(db.Integer, default=21)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    progress = db.relationship(
        'Progress',
        backref='habit',
        lazy=True,
        cascade='all, delete-orphan'
    )

    def current_streak(self):
        """Calculate current streak for the habit."""
        calculator = (DailyStreakCalculator() if self.periodicity == 'daily'
                      else WeeklyStreakCalculator())
        return calculator.calculate(self.progress)

    def completion_rate(self):
        """Calculate completion rate percentage."""
        completed = len([p for p in self.progress if p.completed])
        total_days = min(
            (datetime.now(timezone.utc).date() - self.created_at.date()).days + 1,
            self.target_days
        )
        return round((completed / total_days) * 100) if total_days > 0 else 0


class Progress(db.Model):
    """Progress tracking model for habits."""

    id = db.Column(db.Integer, primary_key=True)
    habit_id = db.Column(db.Integer, db.ForeignKey('habit.id'), nullable=False)
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    completed = db.Column(db.Boolean, default=False)