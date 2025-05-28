"""Route to render the user's dashboard showing all habits."""

from flask import render_template
from flask_login import login_required, current_user
from habits import habits_bp


@habits_bp.route("/")
@login_required
def dashboard():
    """Render dashboard with all habits and their statistics."""
    habits = current_user.habits
    for habit in habits:
        # Precompute values for display in template
        habit.current_streak_value = habit.current_streak()
        habit.completion_rate_value = habit.completion_rate()
    return render_template("dashboard.html", habits=habits)
