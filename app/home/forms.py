from flask import session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, Field, TextAreaField
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


class LoginForm(FlaskForm):
    username = StringField(
        label='用户名：',
        validators=[
            DataRequired(message='用户名不能为空！'),
            Length(min=3, max=50, message='用户名长度必须在3-50位之间'),
        ],
        description='用户名',
        render_kw={
            'type': 'text',
            'placeholder': '用户名',
            'class': 'validate-username',
            'size': 38,
            'maxlength': 99,
        }
    )
    password = PasswordField(
        label='密码：',
        validators=[
            DataRequired("密码不能为空！"),
            Length(min=3, message="密码长度不少于6位")
        ],
        description='密码',
        render_kw={
            'type': 'password',
            'placeholder': '密码',
            'class': 'validate-password',
            'size': 38,
            'maxlength': 99,
        }
    )
    verify_code = StringField(
        label='验证码：',
        validators=[
            DataRequired(),
        ],
        render_kw={
            'class': 'validate-code',
            'size': 18,
            'maxlength': 4,
        }
    )
    submit = SubmitField(
        label='登录',
        render_kw={
            'class': 'btn btn-primary login',
        }
    )


class PasswordForm(FlaskForm):
    old_password = PasswordField(
        label="原始密码 ：",
        validators=[
            DataRequired("原始密码不能为空！")
        ],
        description="原始密码",
        render_kw={
            "placeholder": "请输入原始密码！",
            "size": 38,
        }
    )
    password = PasswordField(
        label="新密码 ：",
        validators=[
            DataRequired("新密码不能为空！")
        ],
        description="新密码",
        render_kw={
            "placeholder": "请输入新密码！",
            "size": 38,
        }
    )
    repassword = PasswordField(
        label="确认密码 ：",
        validators=[
            DataRequired("请输入确认密码！"),
            EqualTo('password', message="两次密码不一致！")
        ],
        description="确认密码",
        render_kw={
            "placeholder": "请输入确认密码！",
            "size": 38,
        }
    )
    submit = SubmitField(
        '确认修改',
        render_kw={
            "class": "btn btn-primary login",
        }
    )

    def validate_old_password(self, field: Field):
        old_password = field.data
        user_id = session['user_id']
        user = User.query.get(int(user_id))
        if not user.check_password(old_password):
            raise ValidationError('原始密码错误！')


class SuggetionForm(FlaskForm):
    """
    意见建议
    """
    name = StringField(
        label="姓名",
        validators=[
            DataRequired("姓名不能为空！")
        ],
        description="姓名",
        render_kw={
            "placeholder": "请输入姓名！",
            "class": "form-control"
        }
    )
    email = StringField(
        label="邮箱",
        validators=[
            DataRequired("邮箱不能为空！")
        ],
        description="邮箱",
        render_kw={
            "type": "email",
            "placeholder": "请输入邮箱！",
            "class": "form-control"
        }
    )
    content = TextAreaField(
        label="意见建议",
        validators=[
            DataRequired("内容不能为空！")
        ],
        description="意见建议",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入内容！",
            "rows": 7
        }
    )
    submit = SubmitField(
        '发送消息',
        render_kw={
            "class": "btn-default btn-cf-submit",
        }
    )
