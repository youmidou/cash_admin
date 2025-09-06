from flask import Blueprint

bp = Blueprint('property', __name__, template_folder='templates')

from app.property import routes
