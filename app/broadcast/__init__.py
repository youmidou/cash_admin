from flask import Blueprint

bp = Blueprint('broadcast', __name__)

from app.broadcast import routes
