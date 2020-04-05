from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from app.admin.views import admin as admin_blueprint
from app.home.views import home as home_blueprint
from config import config


db = SQLAlchemy()


def create_app(config_name: str) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    app.register_blueprint(home_blueprint)
    app.register_blueprint(admin_blueprint)
    db.init_app(app=app)

    return app
