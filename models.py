from db import db
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(db.Model, UserMixin):
    """User model representing application users."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    habits = db.relationship('Habit', backref='user', lazy=True)

    def set_password(self, password):
        """Hash and set the user's password."""
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """Verify if the provided password matches the stored hash."""
        return check_password_hash(self.password, password)


class Habit(db.Model):
    """Habit model representing user habits and their tracking."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)  # Name of the habit
    periodicity = db.Column(db.String(20), default='daily')  # e.g., daily, weekly
    target_days = db.Column(db.Integer, default=21)  # Target days for completion
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Creation timestamp
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Owner reference
    progress = db.relationship('Progress', backref='habit', lazy=True)  # Progress entries

    def current_streak(self):
        """
        Calculate the current streak of consecutive completed days.
        
        Returns:
            int: Number of days in the current streak
        """
        if not self.progress:
            return 0

        # Sort progress entries by date (newest first)
        sorted_entries = sorted(self.progress, key=lambda x: x.date, reverse=True)
        today = datetime.utcnow().date()
        streak = 0

        # Check today's entry first
        today_entry = next((e for e in sorted_entries if e.date == today), None)
        if today_entry and today_entry.completed:
            streak = 1
            current_date = today - timedelta(days=1)  # Move to previous day
        else:
            current_date = today - timedelta(days=1)  # Start from yesterday

        # Check previous days in sequence
        for entry in sorted_entries[1:]:
            if entry.completed and entry.date == current_date:
                streak += 1
                current_date -= timedelta(days=1)  # Move back one more day
            else:
                break  # Streak broken

        return streak

    def completion_rate(self):
        """
        Calculate the habit completion percentage.
        
        Returns:
            int: Completion percentage (0-100)
        """
        completed = len([p for p in self.progress if p.completed])
        # Calculate total days either since creation or target days, whichever is smaller
        total_days = min(
            (datetime.utcnow().date() - self.created_at.date()).days + 1,
            self.target_days
        )
        return round((completed / total_days) * 100) if total_days > 0 else 0


class Progress(db.Model):
    """Progress model representing daily habit completion status."""
    id = db.Column(db.Integer, primary_key=True)
    habit_id = db.Column(db.Integer, db.ForeignKey('habit.id'), nullable=False)  # Habit reference
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow)  # Date of record
    completed = db.Column(db.Boolean, default=False)  # Completion status