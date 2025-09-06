from flask import Blueprint

bp = Blueprint('reward', __name__)

from app.reward import routes
