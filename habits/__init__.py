"""Blueprint initialization and route registration for the habits module."""

from flask import Blueprint

habits_bp = Blueprint("habits", __name__)

# Register route modules to bind routes to the blueprint
from .routes import dashboard, add, detail, delete, mark, api
