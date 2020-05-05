from decimal import Decimal
from functools import wraps

from flask import Blueprint, render_template, session, redirect, url_for, flash, request, jsonify
from sqlalchemy import or_
from werkzeug.security import generate_password_hash

from app import db
from app.admin.forms import AdminLoginForm, GoodsForm
from app.models import Admin, Goods, SuperCat, SubCat, User

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


@admin.route('/logout')
@admin_login
def logout():
    session.pop('admin', None)
    session.pop('admin_id', None)
    return redirect(url_for('admin.login'))


@admin.route('/create_superuser')
def create_superuser():
    admin = Admin()
    admin.manager = 'admin'
    admin.password = generate_password_hash('123')
    db.session.add(admin)
    db.session.commit()
    return redirect(url_for('admin.login'))


@admin.route('/goods/del_confirm')
def goods_del_confirm():
    goods_id = request.args.get('goods_id')
    goods = Goods.query.filter_by(id=goods_id).first_or_404()
    return render_template('admin/goods_del_confirm.html', goods=goods)


@admin.route('/goods/del/<int:id>', methods=['GET'])
def goods_del(id: int = None):
    goods = Goods.query.get(id)
    db.session.delete(goods)
    db.session.commit()
    return redirect(url_for('admin.index', page=1))


@admin.route('/goods/add', methods=['GET', 'POST'])
def goods_add():
    form = GoodsForm()
    supercat_list = [(item.id, item.cat_name) for item in SuperCat.query.all()]
    form.supercat_id.choices = supercat_list
    subcat_list = [(item.id, item.cat_name) for item in SubCat.query.all()]
    form.subcat_id.choices = subcat_list
    if form.validate_on_submit():
        goods = Goods(
            name=form.name.data,
            original_price=Decimal(form.original_price.data).quantize(Decimal('0.00')),
            current_price=Decimal(form.original_price.data).quantize(Decimal('0.00')),
            picture=form.picture.data,
            introduction=form.introduction.data,
            is_sale=int(form.is_sale.data),
            is_new=int(form.is_new.data),
            supercat_id=int(form.supercat_id.data),
            subcat_id=int(form.subcat_id.data),
        )
        db.session.add(goods)
        db.session.commit()
        return redirect(url_for('admin.index'))
    return render_template('admin/goods_add.html', form=form)


@admin.route('/goods/select_sub_cat', methods=['GET'])
def select_sub_cat():
    supercat_id = request.args.get('supercat_id', 0)
    subcats = SubCat.query.filter_by(super_cat_id=supercat_id).all()
    result = {}
    if subcats:
        data = []
        for item in subcats:
            data.append({'id': item.id, 'cat_name': item.cat_name})
        result['status'] = 1
        result['message'] = 'ok'
        result['data'] = data
    else:
        result['status'] = 0
        result['message'] = 'error'
    return jsonify(result)


@admin.route('/goods/edit/<int:id>', methods=['GET', 'POST'])
def goods_edit(id: int):
    goods = Goods.query.get_or_404(id)
    form = GoodsForm()
    form.supercat_id.choices = [(v.id, v.cat_name) for v in SuperCat.query.all()]
    form.subcat_id.choices = [(v.id, v.cat_name) for v in SubCat.query.filter_by(super_cat_id=goods.supercat_id).all()]
    if request.method == 'GET':
        form.name.data = goods.name
        form.supercat_id.data = goods.supercat_id
        form.subcat_id.data = goods.subcat_id
        form.original_price.data = goods.original_price
        form.picture.data = goods.picture
        form.is_new.data = goods.is_new
        form.is_sale.data = goods.is_sale
        form.introduction.data = goods.introduction
    elif form.validate_on_submit():
        goods.name = form.name.data
        goods.supercat_id = form.supercat_id.data
        goods.subcat_id = form.subcat_id.data
        goods.original_price = form.original_price.data
        goods.picture = form.picture.data
        goods.is_new = form.is_new.data
        goods.is_sale = form.is_sale.data
        goods.introduction = form.introduction.data
        db.session.add(goods)
        db.session.commit()
        return redirect(url_for('admin.index'))
    return render_template('admin/goods_edit.html', goods_id=id, form=form)


@admin.route('/')
def topgoods():
    return None


@admin.route('/user/list')
@admin_login
def user_list():
    page = request.args.get('page', 1, type=int)
    keyword = request.args.get('keyword', '', type=str)
    if keyword:
        filters = or_(User.username == keyword, User.password == keyword)
        page_data = User.query.filter(filters)\
            .order_by(User.addtime.desc())\
            .paginate(page=page, per_page=5)
    else:
        page_data = User.query.order_by(User.addtime.desc())\
            .paginate(page=page, per_page=5)
    return render_template('admin/user_list.html', page_data=page_data)


@admin.route('/')
@admin_login
def orders_list():
    return None


@admin.route('/')
@admin_login
def supercat_list():
    return None


@admin.route('/')
@admin_login
def subcat_list():
    return None


@admin.route('/')
@admin_login
def goods_detail():
    return None

