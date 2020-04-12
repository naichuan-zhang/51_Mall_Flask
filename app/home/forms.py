from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, Field
from wtforms.validators import DataRequired, Length, Regexp, Email, EqualTo, ValidationError

from app.models import User


class RegisterForm(FlaskForm):
    username = StringField(
        label='用户名：',
        validators=[
            DataRequired(message='用户名不能为空！'),
            Length(min=3, max=50, message='用户名长度必须在3-50位之间')
        ],
        description='用户名',
        render_kw={
            'type': 'text',
            'placeholder': '用户名',
            'class': 'validate-username',
            'size': 38,
        }
    )
    phone = StringField(
        label='联系电话：',
        validators=[
            DataRequired(message='手机号不能为空！'),
            Regexp("1[34578][0-9]{9}", message='手机号格式不正确')
        ],
        description='手机号',
        render_kw={
            'type': 'text',
            'placeholder': '联系电话',
            'size': 38,
        }
    )
    email = StringField(
        label='邮箱：',
        validators=[
            DataRequired(message='邮箱不能为空！'),
            Email(message='邮箱格式不正确'),
        ],
        description='邮箱',
        render_kw={
            'type': 'email',
            'placeholder': '邮箱',
            'size': 38,
        }
    )
    password = PasswordField(
        label='密码：',
        validators=[
            DataRequired(message='密码不能为空！'),
        ],
        description='密码',
        render_kw={
            'placeholder': '密码',
            'size': 38,
        }
    )
    re_password = PasswordField(
        label='确认密码：',
        validators=[
            DataRequired(message='请确认输入密码！'),
            EqualTo('password', message='两次输入密码不一致'),
        ],
        description='确认密码',
        render_kw={
            'placeholder': '确认密码',
            'size': 38,
        }
    )
    submit = SubmitField(
        label='同意协议并注册',
        render_kw={
            'class': 'btn btn-primary login',
        }
    )

    def validate_email(self, field: Field):
        email = field.data
        user_count = User.query.filter_by(email=email).count()
        if user_count >= 1:
            raise ValidationError('邮箱已存在！')

    def validate_phone(self, field: Field):
        phone = field.data
        user_count = User.query.filter_by(phone=phone).count()
        if user_count >= 1:
            raise ValidationError('手机号已存在!')
