from flask import Blueprint


profile = Blueprint('profiles', __name__)

from . import routes
