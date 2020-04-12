from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import config


db = SQLAlchemy()


def create_app(config_name: str) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    from app.admin.views import admin as admin_blueprint
    from app.home.views import home as home_blueprint

    app.register_blueprint(home_blueprint)
    app.register_blueprint(admin_blueprint)
    db.init_app(app=app)

    # init database when app is created
    from . import models
    with app.test_request_context():
        db.create_all()

    return app
