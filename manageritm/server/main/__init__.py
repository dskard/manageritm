from flask import Blueprint

bp = Blueprint('main', __name__)

from manageritm.server.main import routes
