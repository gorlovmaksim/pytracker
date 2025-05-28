"""API endpoint to update progress from the frontend asynchronously."""

from flask import request, jsonify
from flask_login import login_required, current_user
from datetime import datetime, timedelta

from db import db
from models import Habit, Progress
from habits import habits_bp


@habits_bp.route("/api/progress", methods=["POST"])
@login_required
def update_progress():
    """Receive progress updates for a habit via AJAX.

    Returns JSON indicating updated streak and completion stats.
    """
    data = request.get_json()
    habit = Habit.query.get_or_404(data["habit_id"])

    if habit.user_id != current_user.id:
        return jsonify({"success": False, "error": "Permission denied"}), 403

    date = datetime.strptime(data["date"], "%Y-%m-%d").date()
    start_date = habit.created_at.date()
    end_date = start_date + timedelta(days=habit.target_days - 1)

    if date < start_date or date > end_date:
        return jsonify({"success": False, "error": "Date outside habit period"}), 400

    progress = Progress.query.filter_by(habit_id=habit.id, date=date).first()

    if not progress:
        progress = Progress(habit_id=habit.id, date=date, completed=data["completed"])
        db.session.add(progress)
    else:
        progress.completed = data["completed"]

    db.session.commit()

    return jsonify(
        {
            "success": True,
            "streak": habit.current_streak(),
            "completion_rate": habit.completion_rate(),
        }
    )
