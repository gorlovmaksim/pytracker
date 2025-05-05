"""Application configuration settings."""

import os


class Config:
    """Base configuration class."""

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-123'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///habits.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False