from flask import Blueprint


admin = Blueprint('admin', __name__)


@admin.route('/admin')
def index():
    return 'hello from admin'
