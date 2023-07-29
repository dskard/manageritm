from flask import Blueprint

bp = Blueprint('client', __name__)

from manageritm.server.client import routes
