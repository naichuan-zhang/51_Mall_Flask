# from app.home import home

from flask import Blueprint


home = Blueprint('home', __name__)


@home.route('/')
def index():
    return 'hello from home'
