import re

import os
from django import forms
from django.core.exceptions import ValidationError
from whatALLsold import settings

from .models import *

def check_password(value):
    if re.match(r'\d+$',value):
        raise ValidationError("密码不能是纯数字")


class UserForm(forms.Form):

    username = forms.CharField(label='会员名称',min_length=6,max_length=30,error_messages={
        'required': '请输入用户名',
        'min_length': '最少6个字符',
        'max_length': '最多30字符',
    })
    password = forms.CharField(label='密码',validators=[check_password],min_length=6, max_length=30, widget=forms.PasswordInput, error_messages={
        'required': '请输入密码',
        'min_length': '最少6个字符',
        'max_length': '最多30字符',
    })
    ugrade = forms.CharField(label='用户积分',error_messages={
        'required':'积分不能为空'
    })
    email = forms.EmailField(label='邮箱',error_messages={
        'required': '请输入邮箱',
        "invalid": "邮箱格式不合法"
    })
    phone = forms.CharField(label='电话',min_length=11,error_messages={
        'min_length':'至少11位'
    })
    province = forms.CharField(label='省',error_messages={
        'required':'请输入省份'
    })
    city = forms.CharField(label='市', error_messages={
        'required': '请输入市'
    })
    district = forms.CharField(label='区', error_messages={
        'required': '请输入区'
    })
    address = forms.CharField(label='详细地址',min_length=5,max_length=40,error_messages={
        'required': '请输入详细地址',
        'min_length': '最少5个字符',
        'max_length': '最多40字符',
    })
    def clean_phone(self):
        value = self.cleaned_data.get('phone')
        if not re.match(r'^1[35678]\d{9}$',value):
            raise ValidationError('手机号码不正确,请重新填写')
        else:
            return value
