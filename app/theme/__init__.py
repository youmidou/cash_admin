from flask import Blueprint

bp = Blueprint('theme', __name__)

from app.theme import routes
