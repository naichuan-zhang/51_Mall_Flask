import random
import string
from io import BytesIO
from typing import Tuple

from PIL import Image, ImageFont, ImageDraw
from flask import render_template, session, redirect, url_for, flash, make_response, request
from werkzeug.security import generate_password_hash

from app.models import Goods, User, Cart
from . import home
from .forms import RegisterForm, LoginForm, PasswordForm
from .. import db


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
    session.pop('user_id', None)
    session.pop('username', None)
    return redirect(url_for('home.login'))


@home.route('/modify_pwd', methods=['GET', 'POST'])
def modify_password():
    form = PasswordForm()
    if form.validate_on_submit():
        new_password = form.password.data
        user = User.query.filter_by(username=session['username']).first()
        user.password = generate_password_hash(new_password)
        db.session.add(user)
        db.session.commit()
        return "<script>alert('密码修改成功！'); location.href='/';</script>"

    return render_template('home/modify_password.html', form=form)


@home.route('/goods_detail/<int:goods_id>')
def goods_detail(goods_id: int):
    user_id = session.get('user_id', 0)
    goods = Goods.query.get_or_404(goods_id)
    type_id = request.args.get('type')
    goods.views_count = goods.views_count + 1
    db.session.add(goods)
    db.session.commit()

    hot_goods = Goods.query.filter_by(subcat_id=goods.subcat_id)\
        .order_by(Goods.views_count.desc()).limit(5).all()
    similar_goods = Goods.query.filter_by(subcat_id=goods.subcat_id)\
        .order_by(Goods.addtime.desc()).limit(5).all()

    return render_template('home/goods_detail.html', goods=goods, user_id=user_id,
                           type_id=type_id, hot_goods=hot_goods, similar_goods=similar_goods)


@home.route('/cart_add')
def cart_add():
    print(request.args.get('user_id'))
    cart = Cart(
        goods_id=request.args.get('goods_id'),
        number=request.args.get('number'),
        user_id=session.get('user_id', 0)   # 用户未登录默认为0
    )
    db.session.add(cart)
    db.session.commit()
    return redirect(url_for('home.shopping_cart'))


@home.route('/shopping_cart')
def shopping_cart():
    return render_template('home/shopping_cart.html')


@home.route('/goods_list')
def goods_list(id: int):
    return None
