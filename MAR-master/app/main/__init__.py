# app/main/__init__.py
from flask import Blueprint

bp = Blueprint('main', __name__)

from app.main import routes  # Import routes to register with the blueprint
