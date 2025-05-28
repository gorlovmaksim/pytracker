"""Route for marking a habit as complete/incomplete for today."""

from flask import redirect, url_for, flash, abort
from flask_login import login_required, current_user
from datetime import datetime
from db import db
from models import Habit, Progress
from habits import habits_bp


@habits_bp.route("/<int:habit_id>/mark/<completed>", methods=["POST"])
@login_required
def mark_habit(habit_id, completed):
    """Mark or unmark the habit for today as complete.

    Args:
        habit_id (int): Habit to update.
        completed (str): 'true' or 'false' string from URL.

    Returns:
        redirect: Back to dashboard.
    """
    habit = Habit.query.get_or_404(habit_id)
    if habit.user_id != current_user.id:
        abort(403)

    today = datetime.utcnow().date()
    progress = Progress.query.filter_by(habit_id=habit.id, date=today).first()

    is_completed = completed == "true"

    if not progress:
        progress = Progress(habit_id=habit.id, date=today, completed=is_completed)
        db.session.add(progress)
    else:
        progress.completed = is_completed

    db.session.commit()
    flash("Habit status updated!", "success")
    return redirect(url_for("habits.dashboard"))
