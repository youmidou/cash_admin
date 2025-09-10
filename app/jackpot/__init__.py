from flask import Blueprint

bp = Blueprint('jackpot', __name__)

from app.jackpot import routes

