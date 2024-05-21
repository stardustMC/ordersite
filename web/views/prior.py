from web import models
from django import forms
from django.core.exceptions import ValidationError
from utils.pager import PagerHtmlModel
from utils.bootstrapform import BootStrapForm
from utils.response import BaseResponse
from django.shortcuts import render, redirect, reverse


class PriorModelForm(BootStrapForm, forms.ModelForm):
    class Meta:
        model = models.Prior
        fields = ['title', 'discount']

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) < 2:
            raise ValidationError('头衔长度不能低于2位')
        return title

    def clean_discount(self):
        discount = self.cleaned_data.get('discount')
        if not 0 < discount < 100:
            raise ValidationError('折扣必须在1-99之间')
        return discount


def customer_prior(request):
    queryset = models.Prior.objects.filter(active=1).all()
    pager = PagerHtmlModel(request, queryset, 10)
    return render(request, 'customer_prior.html', context={'pager': pager})


def prior_edit(request, pk):
    obj = models.Prior.objects.get(id=pk)
    if request.method == 'GET':
        form = PriorModelForm(instance=obj)
        return render(request, 'form.html', context={
            'form': form,
        })
    elif request.method == 'POST':
        form = PriorModelForm(instance=obj, data=request.POST)
        if not form.is_valid():
            return render(request, 'form.html', context={
                'form': form,
            })
        form.save()
        return redirect(reverse(viewname='customer_prior'))


def prior_delete(request, pk):
    exist = models.Customer.objects.filter(prior_id=pk, active=1).select_related('prior').exists()
    if exist:
        return BaseResponse(False, details='当前级别下存在用户，无法删除').as_json()
    models.Prior.objects.filter(id=pk).update(active=0)
    return BaseResponse(True, details="").as_json()


def prior_add(request):
    if request.method == 'GET':
        form = PriorModelForm()
        return render(request, 'form.html', context={'form': form})
    elif request.method == 'POST':
        form = PriorModelForm(data=request.POST)
        if not form.is_valid():
            return render(request, 'form.html', context={'form': form})

        form.save()
        return redirect(reverse(viewname='customer_prior'))
