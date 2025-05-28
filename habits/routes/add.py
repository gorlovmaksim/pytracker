"""Route for adding a new habit.

This module handles both GET and POST requests for creating new habits.
Includes form validation and database persistence.
"""

from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from typing import Union, Tuple

from habits import habits_bp
from forms import HabitForm
from db import db
from habits.factory import HabitFactory


@habits_bp.route("/add", methods=["GET", "POST"])
@login_required
def add_habit() -> Union[str, Tuple[str, int]]:
    """Handle adding a new habit.

    GET: Render the habit creation form
    POST: Process form submission and create habit

    Returns:
        Union[str, Tuple[str, int]]:
            - On GET: Rendered template
            - On success: Redirect to dashboard
            - On error: Rendered template with error messages
    """
    form = HabitForm()

    if form.validate_on_submit():
        try:
            habit = HabitFactory.create(
                form.name.data,
                form.periodicity.data,
                current_user.id,
                form.target_days.data,
            )
            db.session.add(habit)
            db.session.commit()
            flash("Habit added successfully!", "success")
            return redirect(url_for("habits.dashboard"))
        except Exception as e:
            db.session.rollback()
            flash("Error adding habit. Please try again.", "danger")
            # Log the error here in production

    return render_template("add_habit.html", form=form)
