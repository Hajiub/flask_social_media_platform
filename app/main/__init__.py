from flask import Blueprint

main = Blueprint('main', __name__, template_folder='main/templates')
from . import routes
