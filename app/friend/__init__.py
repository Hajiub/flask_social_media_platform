from flask import Blueprint

friend  = Blueprint('friend', __name__ )
from . import routes