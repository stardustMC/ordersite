import re
import json
from web import models
from django import forms
from utils import bootstrapform
from django.conf import settings
from utils.emails import send_email
from utils.response import BaseResponse
from django_redis import get_redis_connection
from django.core.exceptions import ValidationError
from utils.encryption import md5_encrypt, random_code
from django.shortcuts import render, redirect, reverse


class LoginForm(bootstrapform.BootStrapForm, forms.Form):

    role = forms.ChoiceField(label="身份", widget=forms.RadioSelect, choices=((1, '管理员'), (2, '用户')))
    username = forms.CharField(label="用户名", strip=True)
    password = forms.CharField(widget=forms.PasswordInput, label="密码")

    def __init__(self, exclude_names=(), *args, **kwargs):
        super().__init__(exclude_names, *args, **kwargs)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username:
            raise ValidationError("用户名不能为空")
        lgt = len(username)
        if not (5 <= lgt <= 12):
            raise ValidationError("用户名长度必须在5-12位之间")
        return username

    def clean_password(self):
        password = self.cleaned_data.get("password")
        if not password:
            raise ValidationError("密码不能为空")
        lgt = len(password)
        if not (5 <= lgt <= 12):
            raise ValidationError("密码长度必须在5-12位之间")
        return password

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if not (username and password):
            raise ValidationError("用户名或密码不规范")
        elif username == password:
            raise ValidationError("用户名不能和密码相同，以防泄露")

        self.cleaned_data['password'] = md5_encrypt(password)
        return self.cleaned_data


class EmailLoginForm(bootstrapform.BootStrapForm, forms.Form):

    role = forms.ChoiceField(label="身份", widget=forms.RadioSelect, choices=((1, '管理员'), (2, '用户')))
    email = forms.EmailField(label="电子邮箱")
    code = forms.CharField(min_length=6, label="验证码", required=False)

    def __init__(self, exclude_names=(), *args, **kwargs):
        super().__init__(exclude_names, *args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        match = re.findall(pattern, email)
        if not match:
            raise ValidationError("非法的邮箱地址")
        return email

    def clean_code(self):
        email = self.cleaned_data.get('email')
        code = self.cleaned_data.get('code')

        conn = get_redis_connection('default')
        auth_code = conn.get(email)

        if not auth_code:
            raise ValidationError("验证码不存在或已过期，请先发送验证码")
        if auth_code.decode('utf-8') != code:
            raise ValidationError("验证码错误！")
        return code


class EmailForm(bootstrapform.BootStrapForm, forms.Form):

    role = forms.ChoiceField(label="身份", widget=forms.RadioSelect, choices=((1, '管理员'), (2, '用户')))
    email = forms.EmailField(label="电子邮箱")

    def clean_email(self):
        email = self.cleaned_data.get('email')
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        match = re.findall(pattern, email)
        if not match:
            raise ValidationError("非法的邮箱地址")
        return email


# Create your views here.
def login(request):
    if request.method == 'GET':
        form = LoginForm(['role'])
        return render(request, 'login.html', context={"form": form})
    elif request.method == 'POST':
        form = LoginForm(data=request.POST)
        if not form.is_valid():
            return BaseResponse(False, details=form.errors.as_json()).as_json()

        user_data = form.cleaned_data
        role = user_data.pop('role')
        if role == '1':
            user = models.Administrator.objects.filter(active=1, **user_data).first()
        else:
            user = models.Customer.objects.filter(active=1, **user_data).first()
        if not user:
            form.add_error("__all__", '用户名或密码不正确')
            return BaseResponse(False, details=form.errors.as_json()).as_json()
        else:
            role_reflection = {
                '1': 'ADMIN',
                '2': 'CUSTOMER',
            }
            request.session[settings.CRC_USER_SESSION_KEY] = json.dumps({
                'role': role_reflection[role],
                'name': user.username,
                'id': user.id,
            })
            return BaseResponse(True, {}).as_json()


def email_send(request):
    form = EmailForm(data=request.GET)
    if not form.is_valid():
        return BaseResponse(False, details='邮箱地址不合法').as_json()

    role = form.cleaned_data['role']
    email = form.cleaned_data['email']
    if role == '1':
        exist = models.Administrator.objects.filter(email=email, active=1).exists()
    else:
        exist = models.Customer.objects.filter(email=email, active=1).exists()
    if not exist:
        return BaseResponse(False, details='邮箱地址未注册或未绑定').as_json()

    code = random_code(6)
    email = form.cleaned_data['email']
    status = send_email(
        sender=settings.CRC_EMAIL_ADDRESS,
        receiver=email,
        title="邮箱登录",
        content="【网站登录】\n您正在通过邮箱登录订单网站，验证码为【{}】，非本人操作请忽略".format(code),
    )
    if not status:
        return BaseResponse(False, details='邮件发送失败，请联系管理员或重试').as_json()

    conn = get_redis_connection('default')
    conn.set(email, code, ex=60)
    return BaseResponse(True, details='').as_json()


def email_login(request):
    if request.method == 'GET':
        form = EmailLoginForm(['role'])
        return render(request, 'email_login.html', context={'form': form})
    elif request.method == 'POST':
        form = EmailLoginForm(['role'], data=request.POST)
        if not form.is_valid():
            return BaseResponse(False, details=form.errors.as_json()).as_json()

        role = form.cleaned_data['role']
        email = form.cleaned_data['email']
        if role == '1':
            user = models.Administrator.objects.filter(active=1, email=email).first()
        else:
            user = models.Customer.objects.filter(active=1, email=email).first()
        role_reflection = {
            '1': 'ADMIN',
            '2': 'CUSTOMER',
        }
        request.session[settings.CRC_USER_SESSION_KEY] = json.dumps({
            'role': role_reflection[role],
            'name': user.username,
            'id': user.id,
        })
        return BaseResponse(True, details="").as_json()


def logout(request):
    request.session.pop(settings.CRC_USER_SESSION_KEY)
    return redirect(reverse(viewname='login'))


def denied(request):
    return render(request, 'denied.html')


def home(request):
    return render(request, 'home.html')


def raw(request):
    return redirect(reverse(viewname='login'))
