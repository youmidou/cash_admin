from flask import Blueprint

bp = Blueprint('stamps', __name__)

from app.stamps import routes
