from flask import render_template, session, redirect, url_for
from werkzeug.security import generate_password_hash

from app.models import Goods, User
from . import home
from .forms import RegisterForm
from .. import db


@home.route('/')
def index():
    hot_goods = Goods.query.order_by(
        Goods.views_count.desc()).limit(2).all()
    new_goods = Goods.query.filter_by(is_new=1)\
        .order_by(Goods.addtime.desc()).limit(12).all()
    sale_goods = Goods.query.filter_by(is_sale=1)\
        .order_by(Goods.addtime.desc()).limit(12).all()

    return render_template('home/index.html', hot_goods=hot_goods, new_goods=new_goods, sale_goods=sale_goods)


@home.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        return redirect(url_for('home.index'))

    form = RegisterForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            password=generate_password_hash(form.password.data),
            phone=form.phone.data,
            email=form.email.data,
        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('home.login'))

    return render_template('home/register.html', form=form)


@home.route('/login')
def login():
    pass


@home.route('/logout')
def logout():
    pass


@home.route('/modify_password')
def modify_password():
    pass
