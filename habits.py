"""Habit tracking blueprint and related functionality."""

from flask import (Blueprint, render_template, redirect, url_for, flash,
                   request, jsonify, abort)
from flask_login import login_required, current_user
from datetime import datetime, timedelta
import json
from db import db
from models import Habit, Progress
from forms import HabitForm


habits_bp = Blueprint('habits', __name__)


class HabitFactory:
    """Factory for creating Habit objects."""

    @staticmethod
    def create(name, periodicity, user_id, target_days):
        """Create a new Habit instance."""
        return Habit(
            name=name,
            periodicity=periodicity,
            user_id=user_id,
            target_days=target_days
        )


@habits_bp.route('/')
@login_required
def dashboard():
    """Display the user's habit dashboard."""
    habits = current_user.habits
    for habit in habits:
        habit.current_streak_value = habit.current_streak()
        habit.completion_rate_value = habit.completion_rate()
    return render_template('dashboard.html', habits=habits)


@habits_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_habit():
    """Add a new habit."""
    form = HabitForm()
    if form.validate_on_submit():
        habit = HabitFactory.create(
            form.name.data,
            form.periodicity.data,
            current_user.id,
            form.target_days.data
        )
        db.session.add(habit)
        db.session.commit()
        flash('Habit added successfully!', 'success')
        return redirect(url_for('habits.dashboard'))
    return render_template('add_habit.html', form=form)


@habits_bp.route('/<int:habit_id>')
@login_required
def habit_detail(habit_id):
    """Display detailed information about a specific habit."""
    habit = Habit.query.get_or_404(habit_id)
    today = datetime.utcnow().date()
    start_date = habit.created_at.date()
    end_date = min(today, start_date + timedelta(days=habit.target_days - 1))
    total_days = (end_date - start_date).days + 1

    progress_data = Progress.query.filter(
        Progress.habit_id == habit_id,
        Progress.date >= start_date,
        Progress.date <= end_date
    ).order_by(Progress.date).all()

    chart_labels = []
    chart_data = []
    for day_offset in range(total_days):
        current_date = start_date + timedelta(days=day_offset)
        chart_labels.append(current_date.strftime('%Y-%m-%d'))
        progress = next((p for p in progress_data if p.date == current_date), None)
        chart_data.append(1 if progress and progress.completed else 0)

    current_day = (today - start_date).days + 1
    completion_rate = round(
        (len([p for p in progress_data if p.completed]) / total_days * 100)
    )

    return render_template(
        'habit_detail.html',
        habit=habit,
        chart_labels=json.dumps(chart_labels),
        chart_data=json.dumps(chart_data),
        today=today,
        current_day=current_day,
        completion_rate=completion_rate,
        total_days=total_days
    )


@habits_bp.route('/<int:habit_id>/delete', methods=['POST'])
@login_required
def delete_habit(habit_id):
    """Delete a habit."""
    habit = Habit.query.get_or_404(habit_id)
    if habit.user_id != current_user.id:
        abort(403)

    try:
        db.session.delete(habit)
        db.session.commit()
        flash('Привычка успешно удалена', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Ошибка при удалении привычки', 'danger')
        app.logger.error(f"Error deleting habit: {str(e)}")

    return redirect(url_for('habits.dashboard'))


@habits_bp.route('/<int:habit_id>/mark/<completed>', methods=['POST'])
@login_required
def mark_habit(habit_id, completed):
    """Mark a habit as completed or skipped."""
    habit = Habit.query.get_or_404(habit_id)
    if habit.user_id != current_user.id:
        abort(403)

    today = datetime.utcnow().date()
    progress = Progress.query.filter_by(
        habit_id=habit.id,
        date=today
    ).first()

    is_completed = completed == 'true'

    if not progress:
        progress = Progress(
            habit_id=habit.id,
            date=today,
            completed=is_completed
        )
        db.session.add(progress)
    else:
        progress.completed = is_completed

    db.session.commit()
    flash('Habit status updated!', 'success')
    return redirect(url_for('habits.dashboard'))


@habits_bp.route('/api/progress', methods=['POST'])
@login_required
def update_progress():
    """Update habit progress via API."""
    data = request.get_json()
    habit = Habit.query.get_or_404(data['habit_id'])

    if habit.user_id != current_user.id:
        return jsonify({'success': False, 'error': 'Permission denied'}), 403

    date = datetime.strptime(data['date'], '%Y-%m-%d').date()
    start_date = habit.created_at.date()
    end_date = start_date + timedelta(days=habit.target_days - 1)

    if date < start_date or date > end_date:
        return jsonify({
            'success': False,
            'error': 'Date outside habit period'
        }), 400

    progress = Progress.query.filter_by(
        habit_id=habit.id,
        date=date
    ).first()

    if not progress:
        progress = Progress(
            habit_id=habit.id,
            date=date,
            completed=data['completed']
        )
        db.session.add(progress)
    else:
        progress.completed = data['completed']

    db.session.commit()

    return jsonify({
        'success': True,
        'streak': habit.current_streak(),
        'completion_rate': habit.completion_rate()
    })