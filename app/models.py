from datetime import datetime

from werkzeug.security import check_password_hash

from . import db


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(255))
    email = db.Column(db.String(50), unique=True)
    phone = db.Column(db.String(), unique=True)
    consumption = db.Column(db.DECIMAL(10, 2), default=0)
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)

    orders = db.relationship('Orders', backref='user')

    def __repr__(self):
        return '<User %r>' % self.username

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Admin(db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)
    manager = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(255))

    def __repr__(self):
        return '<Admin %r>' % self.manager

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Orders(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    # one order only have one user_id
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    receiver_name = db.Column(db.String(50))
    receiver_addr = db.Column(db.String(100))
    receiver_tel = db.Column(db.String(50))
    remark = db.Column(db.String(100))
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)

    orders_detail = db.relationship('OrdersDetail', backref='orders')

    def __repr__(self):
        return '<Order %r>' % self.id


class Cart(db.Model):
    __tablename__ = 'cart'
    id = db.Column(db.Integer, primary_key=True)
    goods_id = db.Column(db.Integer, db.ForeignKey('goods.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    number = db.Column(db.Integer, default=0)
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)

    def __repr__(self):
        return '<Cart %r>' % self.id


# 大分类
class SuperCat(db.Model):
    __tablename__ = 'supercat'
    id = db.Column(db.Integer, primary_key=True)
    cat_name = db.Column(db.String(100))
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)

    subcat = db.relationship('SubCat', backref='supercat')
    goods = db.relationship('Goods', backref='supercat')

    def __repr__(self):
        return '<SuperCat %r>' % self.cat_name


class SubCat(db.Model):
    __tablename__ = "subcat"
    id = db.Column(db.Integer, primary_key=True)
    cat_name = db.Column(db.String(100))
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)
    super_cat_id = db.Column(db.Integer, db.ForeignKey('supercat.id'))

    goods = db.relationship("Goods", backref='subcat')

    def __repr__(self):
        return "<SubCat %r>" % self.cat_name


class Goods(db.Model):
    __tablename__ = 'goods'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    original_price = db.Column(db.DECIMAL(10, 2))
    current_price = db.Column(db.DECIMAL(10, 2))
    picture = db.Column(db.String(255))
    introduction = db.Column(db.Text)
    views_count = db.Column(db.Integer, default=0)
    is_sale = db.Column(db.Boolean(), default=False)
    is_new = db.Column(db.Boolean(), default=False)
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)
    # 所属大分类
    supercat_id = db.Column(db.Integer, db.ForeignKey('supercat.id'))
    # 所属小分类
    subcat_id = db.Column(db.Integer, db.ForeignKey('subcat.id'))

    cart = db.relationship('Cart', backref='goods')
    orders_detail = db.relationship('OrdersDetail', backref='goods')

    def __repr__(self):
        return '<Goods %r>' % self.name


class OrdersDetail(db.Model):
    __tablename__ = 'orders_detail'
    id = db.Column(db.Integer, primary_key=True)
    # 所属商品
    goods_id = db.Column(db.Integer, db.ForeignKey('goods.id'))
    # 所属订单
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    number = db.Column(db.Integer, default=0)

    def __repr__(self):
        return '<OrdersDetail %r>' % self.id
