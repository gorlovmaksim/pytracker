"""Detailed route to visualize habit progress including a graph."""

from flask import render_template
from flask_login import login_required
from datetime import datetime, timedelta
import json

from habits import habits_bp
from models import Habit, Progress


@habits_bp.route("/<int:habit_id>")
@login_required
def habit_detail(habit_id):
    """Show detailed view of a habit including calendar progress.

    Returns a chart of streaks and completion values.
    """
    habit = Habit.query.get_or_404(habit_id)
    today = datetime.utcnow().date()
    start_date = habit.created_at.date()
    end_date = min(today, start_date + timedelta(days=habit.target_days - 1))
    total_days = (end_date - start_date).days + 1

    progress_data = (
        Progress.query.filter(
            Progress.habit_id == habit_id,
            Progress.date >= start_date,
            Progress.date <= end_date,
        )
        .order_by(Progress.date)
        .all()
    )

    chart_labels = []
    chart_data = []
    for day_offset in range(total_days):
        current_date = start_date + timedelta(days=day_offset)
        chart_labels.append(current_date.strftime("%Y-%m-%d"))
        progress = next((p for p in progress_data if p.date == current_date), None)
        chart_data.append(1 if progress and progress.completed else 0)

    current_day = (today - start_date).days + 1
    completion_rate = round(
        (len([p for p in progress_data if p.completed]) / total_days) * 100
    )

    return render_template(
        "habit_detail.html",
        habit=habit,
        chart_labels=json.dumps(chart_labels),
        chart_data=json.dumps(chart_data),
        today=today,
        current_day=current_day,
        completion_rate=completion_rate,
        total_days=total_days,
    )
