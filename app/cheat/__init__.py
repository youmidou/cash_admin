from flask import Blueprint

bp = Blueprint('cheat', __name__)

from app.cheat import routes
