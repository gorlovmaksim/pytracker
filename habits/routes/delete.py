"""Route for securely deleting a user's habit."""

from flask import redirect, url_for, flash, abort, current_app
from flask_login import login_required, current_user
from db import db
from models import Habit
from habits import habits_bp


@habits_bp.route("/<int:habit_id>/delete", methods=["POST"])
@login_required
def delete_habit(habit_id):
    """Allow user to delete one of their habits.

    Args:
        habit_id (int): ID of the habit to delete.

    Returns:
        redirect: Back to dashboard.
    """
    habit = Habit.query.get_or_404(habit_id)
    if habit.user_id != current_user.id:
        abort(403)

    try:
        db.session.delete(habit)
        db.session.commit()
        flash("Habit deleted successfully.", "success")
    except Exception as e:
        db.session.rollback()
        flash("Error deleting habit.", "danger")
        current_app.logger.error(f"Error deleting habit: {str(e)}")

    return redirect(url_for("habits.dashboard"))
