import random
import string
from io import BytesIO
from typing import Tuple

from PIL import Image, ImageFont, ImageDraw
from flask import render_template, session, redirect, url_for, flash, make_response
from werkzeug.security import generate_password_hash

from app.models import Goods, User
from . import home
from .forms import RegisterForm, LoginForm
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


@home.route('/code')
def get_code():
    image, code = get_verify_code()
    buf = BytesIO()
    image.save(buf, 'jpeg')
    buf_str = buf.getvalue()
    response = make_response(buf_str)
    response.headers['Content-Type'] = 'image/gif'
    session['image'] = code
    return response


@home.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('home.index'))

    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        verify_code = form.verify_code.data
        user = User.query.filter_by(username=username).first()

        if user is None:
            flash('用户名不存在！', 'err')
            return render_template('home/login.html', form=form)

        if not user.check_password(password):
            flash('密码错误！', 'err')
            return render_template('home/login.html', form=form)

        if session.get('image').lower() != verify_code.lower():
            flash('验证码错误！', 'err')
            return render_template('home/login.html', form=form)

        session['user_id'] = user.id
        session['username'] = user.username
        return redirect(url_for('home.index'))

    return render_template('home/login.html', form=form)


@home.route('/logout')
def logout():
    pass


@home.route('/modify_password')
def modify_password():
    pass


def get_verify_code() -> Tuple:
    code = generate_text()
    width, height = 120, 50
    img = Image.new('RGB', (width, height), 'white')
    font = ImageFont.truetype(font='app/static/fonts/arial.ttf', size=40)
    draw = ImageDraw.Draw(img)
    for item in range(4):
        draw.text((5 + random.randint(-3, 3) + 23 * item, 5 + random.randint(-3, 3)),
                  text=code[item], fill=generate_color(), font=font)
    return img, code


def generate_text() -> str:
    letters_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_digits) for i in range(4))


def generate_color() -> Tuple:
    return random.randint(32, 127), random.randint(32, 127), random.randint(32, 127)

