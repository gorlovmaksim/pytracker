"""
Example configuration file.

Rename this file to 'config.py' and replace the placeholder values
with your actual secret settings.
"""

import os


class Config:
    """Base configuration class.

    Contains configuration settings for the application.
    """

    SECRET_KEY = os.environ.get("SECRET_KEY") or "insert-your-secret-key"
    SQLALCHEMY_DATABASE_URI = "sqlite:///habits.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
