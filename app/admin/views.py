from flask import Blueprint, render_template

admin = Blueprint('admin', __name__, url_prefix='/admin')


@admin.route('/login')
def login():
    return render_template('admin/login.html')
