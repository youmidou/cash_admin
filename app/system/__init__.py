from flask import Blueprint

bp = Blueprint('system', __name__, url_prefix='/system')

from app.system import routes

