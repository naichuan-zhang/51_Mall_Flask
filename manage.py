import os

from flask import render_template
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Shell

from app import create_app

env_config = os.environ.get("FLASK_ENV", "default")


def make_shell_context():
    return None


app = create_app(config_name=env_config)
manager = Manager(app=app)
migrate = Migrate(app=app)

manager.add_command('db', MigrateCommand(app=app))
manager.add_command('shell', Shell(make_context=make_shell_context))


@app.errorhandler(404)
def page_not_found(error):
    return render_template('home/404.html'), 404


if __name__ == '__main__':
    manager.run()
