from functools import wraps

from flask import Blueprint, render_template, session, redirect, url_for, flash, request
from werkzeug.security import generate_password_hash

from app import db
from app.admin.forms import AdminLoginForm
from app.models import Admin, Goods

admin = Blueprint('admin', __name__, url_prefix='/admin')


def admin_login(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'admin' not in session:
            return redirect(url_for('admin.login'))
        return f(*args, **kwargs)
    return wrap


@admin.route('/')
@admin_login
def index():
    page = request.args.get('page', 1, type=int)
    page_data = Goods.query.order_by(Goods.addtime.desc())\
        .paginate(page=page, per_page=10)
    return render_template('admin/index.html', page_data=page_data, page=page)


@admin.route('/login', methods=['GET', 'POST'])
def login():
    count = Admin.query.filter_by(manager='admin').count()
    if count == 0:
        return redirect(url_for('admin.create_superuser'))
    if 'admin' in session:
        return redirect(url_for('admin.index'))

    form = AdminLoginForm()
    if form.validate_on_submit():
        manager = form.manager.data
        password = form.password.data
        admin = Admin.query.filter_by(manager=manager).first()
        if not admin:
            flash('用户名错误！', 'err')
            return redirect(url_for('admin.login'))
        if not admin.check_password(password):
            flash('密码错误！', 'err')
            return redirect(url_for('admin.login'))
        session['admin'] = manager
        session['admin_id'] = admin.id
        return redirect(url_for("admin.index"))
    return render_template("admin/login.html", form=form)


@admin.route('/create_superuser')
def create_superuser():
    admin = Admin()
    admin.manager = 'admin'
    admin.password = generate_password_hash('123')
    db.session.add(admin)
    db.session.commit()
    return redirect(url_for('admin.login'))
