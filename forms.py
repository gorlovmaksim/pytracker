"""Form definitions for user authentication and habit tracking."""

from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    SelectField,
    IntegerField
)
from wtforms.validators import (
    DataRequired,
    Email,
    Length,
    EqualTo
)


class RegistrationForm(FlaskForm):
    """User registration form."""

    username = StringField(
        'Username',
        validators=[
            DataRequired(),
            Length(min=4, max=20)
        ]
    )
    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email()
        ]
    )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=6)
        ]
    )
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[
            DataRequired(),
            EqualTo('password')
        ]
    )


class LoginForm(FlaskForm):
    """User login form."""

    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email()
        ]
    )
    password = PasswordField(
        'Password',
        validators=[DataRequired()]
    )


class HabitForm(FlaskForm):
    """Habit creation form."""

    name = StringField(
        'Habit Name',
        validators=[DataRequired()]
    )
    periodicity = SelectField(
        'Periodicity',
        choices=[
            ('daily', 'Daily'),
            ('weekly', 'Weekly')
        ],
        validators=[DataRequired()]
    )
    target_days = IntegerField(
        'Target Days',
        default=21,
        validators=[DataRequired()]
    )