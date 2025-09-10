from flask import Blueprint

bp = Blueprint('quest', __name__, template_folder='templates')

from app.quest import routes

