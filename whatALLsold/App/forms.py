import hashlib
import re

from django import forms
from django.contrib.sessions.models import Session
from django.core.exceptions import ValidationError


from App.models import User


def check_password(value):
    if re.match(r'\d+$',value):
        raise ValidationError("密码不能是纯数字")
    if " " in value:
        raise ValidationError("密码不能有空格")


def check_username(value):
    if User.objects.filter(username=value).exists():
        raise ValidationError("用户名已存在")
    if " " in value:
        raise ValidationError("用户名不能有空格")


def check_yzm(value):
    res = Session.objects.all()[0]
    yzm = res.get_decoded().get("yzm")
    print(yzm, value)
    if value.isdigit():
        if yzm != int(value):
            raise ValidationError("验证码错误")
    else:
        raise ValidationError("验证码错误")


def check_phone(value):
    if not re.match(r"1[35678]\d{9}$", value):
        raise ValidationError("请输入正确的手机号")


class RegForm(forms.Form):
    username = forms.CharField(label="用户名",validators=[check_username], min_length=6, max_length=30, error_messages={
        'required': '请输入用户名',
        'min_length': '最少6个字符',
        'max_length': '最多30字符',
    })
    password = forms.CharField(label="密码", validators=[check_password], min_length=6, max_length=30, widget=forms.PasswordInput, error_messages={
        'required': '请输入密码',
        'min_length': '最少6个字符',
        'max_length': '最多30字符',
    })
    confirm_password = forms.CharField(label="确认密码", min_length=6, max_length=30, widget=forms.PasswordInput, error_messages={
        'required': '请确认密码',
        'min_length': '最少6个字符',
        'max_length': '最多30字符',
    })
    email = forms.EmailField(label="邮箱", error_messages={'required': '请输入邮箱',"invalid":"邮箱格式不合法"})
    phone = forms.CharField(label='手机', min_length=11, validators=[check_phone], error_messages={'required': '请输入手机号'})
    yzm = forms.CharField(label="验证码", validators=[check_yzm], error_messages={"required":"请输入验证码"})

    def clean(self):
        password1 = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("confirm_password")
        if password1 != password2:
            raise ValidationError({"confirm_password":"两次密码不一致"})
        else:
            return self.cleaned_data


class LoginForm(forms.Form):
    username = forms.CharField(label="用户名")
    password = forms.CharField(label="密码", widget=forms.PasswordInput)

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        password = hashlib.sha1(password.encode("utf8")).hexdigest()
        if not User.objects.filter(username=username, password=password).exists():
            raise ValidationError({"password":"用户名或密码错误"})
        else:
            return self.cleaned_data


class GetpasswordForm(forms.Form):
    username = forms.CharField(label="用户名", error_messages={'required': '请输入用户名'})
    password = forms.CharField(label="密码", validators=[check_password], min_length=6, max_length=30, widget=forms.PasswordInput, error_messages={
        'required': '请输入密码',
        'min_length': '最少6个字符',
        'max_length': '最多30字符',
    })
    confirm_password = forms.CharField(label="确认密码", min_length=6, max_length=30, widget=forms.PasswordInput, error_messages={
        'required': '请确认密码',
        'min_length': '最少6个字符',
        'max_length': '最多30字符',
    })
    email = forms.EmailField(label="邮箱", error_messages={'required': '请输入邮箱',"invalid":"邮箱格式不合法"})
    yzm = forms.CharField(label="验证码", validators=[check_yzm], error_messages={"required":"请输入验证码"})

    def clean(self):
        password1 = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("confirm_password")
        if password1 != password2:
            raise ValidationError({"confirm_password":"两次密码不一致"})
        else:
            return self.cleaned_data


    def clean_username(self):
        print(self.cleaned_data)
        username = self.cleaned_data.get("username")
        if not User.objects.filter(username=username).exists():
            raise ValidationError("用户名不存在, 请重新输入")
        return username


