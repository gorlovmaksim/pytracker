"""Authentication blueprint for user registration and login.

This module handles:
- User registration
- User login
- User logout
"""

from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from typing import Union, Tuple

from models import User
from forms import LoginForm, RegistrationForm
from db import db

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["GET", "POST"])
def register() -> Union[str, Tuple[str, int]]:
    """Handle user registration.

    GET: Render registration form
    POST: Process registration form

    Returns:
        Union[str, Tuple[str, int]]:
            - On GET: Rendered template
            - On success: Redirect to login
            - On error: Rendered template with error messages
    """
    form = RegistrationForm()

    if form.validate_on_submit():
        try:
            user = User(username=form.username.data, email=form.email.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash("Registration successful! Please log in.", "success")
            return redirect(url_for("auth.login"))
        except Exception as e:
            db.session.rollback()
            flash("Registration failed. Please try again.", "danger")
            # Log the error here in production

    return render_template("register.html", form=form)


@auth_bp.route("/login", methods=["GET", "POST"])
def login() -> Union[str, Tuple[str, int]]:
    """Handle user login.

    GET: Render login form
    POST: Process login form

    Returns:
        Union[str, Tuple[str, int]]:
            - On GET: Rendered template
            - On success: Redirect to dashboard
            - On error: Rendered template with error messages
    """
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash("Logged in successfully!", "success")
            return redirect(url_for("habits.dashboard"))
        flash("Invalid email or password", "danger")

    return render_template("login.html", form=form)


@auth_bp.route("/logout")
@login_required
def logout() -> Tuple[str, int]:
    """Handle user logout.

    Returns:
        Tuple[str, int]: Redirect to login page with status code
    """
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.login"))
