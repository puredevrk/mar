# app/auth/__init__.py
from flask import Blueprint

bp = Blueprint('auth', __name__)

from app.auth import routes  # Import routes to register with the blueprint
