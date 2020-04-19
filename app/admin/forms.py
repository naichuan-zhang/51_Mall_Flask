from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, Field
from wtforms.validators import DataRequired, ValidationError

from app.models import Admin


class AdminLoginForm(FlaskForm):
    manager = StringField(
        label="管理员名",
        validators=[
            DataRequired("管理员名不能为空")
        ],
        description="管理员名",
        render_kw={
            "class": "manager",
            "placeholder": "请输入管理员名！",
        }
    )
    password = PasswordField(
        label="密码",
        validators=[
            DataRequired("密码不能为空")
        ],
        description="密码",
        render_kw={
            "class": "password",
            "placeholder": "请输入密码！",
        }
    )
    submit = SubmitField(
        '登录',
        render_kw={
            "class": "login_ok",
        }
    )

    def validate_manager(self, field: Field):
        manager = field.data
        count = Admin.query.filter_by(manager=manager).count()
        if count == 0:
            raise ValidationError('该管理员不存在！')
