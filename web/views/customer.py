import re
from web import models
from django import forms
from django.db.models import Q
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect, reverse
from utils.pager import PagerHtmlModel
from utils.encryption import md5_encrypt
from utils.bootstrapform import BootStrapForm
from utils.filter_reverse import filter_reverse
from utils.response import BaseResponse


class CustomerModelForm(BootStrapForm, forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="密码")
    re_password = forms.CharField(widget=forms.PasswordInput, label="确认密码")

    class Meta:
        model = models.Customer
        fields = ['username', 'password', 're_password', 'phone', 'prior']
        error_messages = {
            'prior': {
                'required': '请选择用户级别'
            }
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username:
            raise ValidationError("用户名不能为空")
        exist = models.Customer.objects.filter(username=username).exists()
        if exist:
            raise ValidationError("用户名已被使用")
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

    def clean_re_password(self):
        password = self.cleaned_data.get("password")
        re_password = self.cleaned_data.get("re_password")
        if password != re_password:
            raise ValidationError("确认密码与原密码不一致")
        return re_password

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        pattern = r'^1\d{10}$'
        result = re.match(pattern, phone)
        if not result:
            raise ValidationError('请输入合法的手机号')
        exist = models.Customer.objects.filter(phone=phone).exists()
        if exist:
            raise ValidationError("手机号已被使用")
        return phone

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if not (username and password):
            raise ValidationError("用户名或密码不规范")
        elif username == password:
            raise ValidationError("用户名不能和密码相同，以防泄露")

        self.cleaned_data['password'] = md5_encrypt(password)
        return self.cleaned_data


class CustomerEditModelForm(BootStrapForm, forms.ModelForm):
    class Meta:
        model = models.Customer
        fields = ['username', 'phone', 'prior']
        error_messages = {
            'prior': {
                'required': '请选择用户级别'
            }
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username:
            raise ValidationError("用户名不能为空")
        lgt = len(username)
        if not (5 <= lgt <= 12):
            raise ValidationError("用户名长度必须在5-12位之间")
        return username

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        pattern = r'^1\d{10}$'
        result = re.match(pattern, phone)
        if not result:
            raise ValidationError('请输入合法的手机号')
        return phone


def customer(request):
    keyword = request.GET.get('keyword')
    con = Q()
    if keyword:
        con.connector = 'OR'
        con.children.append(('username__contains', keyword))
        con.children.append(('phone__contains', keyword))
        con.children.append(('prior__title__contains', keyword))
    queryset = models.Customer.objects.filter(con).filter(active=1).all()
    pager = PagerHtmlModel(request, queryset, 10)
    return render(request, 'customer.html', context={
        'pager': pager,
        'keyword': "" if keyword is None else keyword
    })


def customer_add(request):
    if request.method == 'GET':
        form = CustomerModelForm(initial={'prior': 1})
        return render(request, 'form.html', context={'form': form})
    elif request.method == 'POST':
        form = CustomerModelForm(data=request.POST)
        if not form.is_valid():
            return render(request, 'form.html', context={'form': form})
        form.instance.creator_id = request.crc_user.id
        form.save()
        return redirect(reverse(viewname='customer'))


def customer_edit(request, pk):
    obj = models.Customer.objects.get(id=pk)
    if request.method == 'GET':
        form = CustomerEditModelForm(instance=obj)
        return render(request, 'form.html', context={'form': form})
    elif request.method == 'POST':
        form = CustomerEditModelForm(instance=obj, data=request.POST)
        if not form.is_valid():
            return render(request, 'form.html', context={'form': form})

        form.save()
        return redirect(filter_reverse(request, reverse(viewname='customer')))


def customer_delete(request, pk):
    if request.is_ajax():
        models.Customer.objects.filter(id=pk).update(active=0)
        return BaseResponse(True, details="").as_json()
    else:
        pass
