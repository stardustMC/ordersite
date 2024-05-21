from web import models
from django import forms
from utils.bootstrapform import BootStrapForm
from django.core.exceptions import ValidationError
from utils.encryption import md5_encrypt
from django.shortcuts import render, redirect, reverse


class CustomerResetPasswordModelForm(BootStrapForm, forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="原密码", error_messages={'required': "该字段为必填项"})
    new_password = forms.CharField(widget=forms.PasswordInput, label="密码", error_messages={'required': "该字段为必填项"})
    re_new_password = forms.CharField(widget=forms.PasswordInput, label="确认密码", error_messages={'required': "该字段为必填项"})

    class Meta:
        model = models.Customer
        fields = ['password', 'new_password', 're_new_password']

    def clean_password(self):
        password = self.cleaned_data.get("password")
        exist = models.Customer.objects.filter(id=self.instance.id, password=md5_encrypt(password)).exists()
        if not exist:
            raise ValidationError("原密码不正确")
        return password

    def clean_new_password(self):
        new_password = self.cleaned_data.get("new_password")
        if not new_password:
            raise ValidationError("密码不能为空")
        lgt = len(new_password)
        if not (5 <= lgt <= 12):
            raise ValidationError("密码长度必须在5-12位之间")
        return new_password

    def clean_re_password(self):
        new_password = self.cleaned_data.get("new_password")
        re_new_password = self.cleaned_data.get("re_new_password")
        if new_password != re_new_password:
            raise ValidationError("确认密码与新密码不一致")
        return re_new_password

    def clean(self):
        re_new_password = self.cleaned_data.get('re_new_password')
        if not re_new_password:
            raise ValidationError("新密码不能为空")
        from utils.encryption import md5_encrypt
        self.cleaned_data['password'] = md5_encrypt(re_new_password)
        return self.cleaned_data


class CustomerProfileForm(BootStrapForm, forms.ModelForm):
    class Meta:
        model = models.Customer
        fields = ['username', 'prior', 'balance', 'phone', 'email']
        help_texts = {
            'username': '用户名不可更改',
            'prior': '会员等级越高享受的折扣越高',
            'balance': '余额可用于创建订单',
            'phone': '11位大陆手机号',
            'email': '可使用邮箱登录',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs['disabled'] = 'disabled'


def my_profile(request):
    cus_obj = models.Customer.objects.filter(id=request.crc_user.id, active=1).first()
    form = CustomerProfileForm(initial=forms.model_to_dict(cus_obj))
    return render(request, 'my_profile.html', context={'form': form})


def my_reset_password(request):
    obj = models.Customer.objects.filter(id=request.crc_user.id).first()
    if request.method == 'GET':
        form = CustomerResetPasswordModelForm(instance=obj)
        return render(request, 'form.html', context={'form': form})
    elif request.method == 'POST':
        form = CustomerResetPasswordModelForm(instance=obj, data=request.POST)
        if not form.is_valid():
            return render(request, 'form.html', context={'form': form})

        form.save()
        return redirect(reverse(viewname='my_profile'))
