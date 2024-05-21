from web import models
from django import forms
from utils.pager import PagerHtmlModel
from utils.response import BaseResponse
from utils.bootstrapform import BootStrapForm
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect, reverse


class PriceModelForm(BootStrapForm, forms.ModelForm):
    class Meta:
        model = models.PricePolicy
        fields = ['price', 'count']

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price < 0:
            raise ValidationError("价格不能低于0")
        return price

    def clean_count(self):
        count = self.cleaned_data.get('count')
        if count < 1000:
            raise ValidationError("播放量最低不能低于1000")
        return count


def price(request):
    if request.method == 'GET':
        queryset = models.PricePolicy.objects.filter(active=1).all()
        pager = PagerHtmlModel(request, queryset, per_page_row=5)
        return render(request, 'price.html', context={"pager": pager})
    elif request.method == "POST":
        pass


def price_add(request):
    if request.method == 'GET':
        form = PriceModelForm()
        return render(request, 'form.html', context={'form': form})
    elif request.method == 'POST':
        form = PriceModelForm(data=request.POST)
        if not form.is_valid():
            return render(request, 'form.html', context={'form': form})
        form.save()
        return redirect(reverse(viewname='price_add'))


def price_edit(request, pk):
    obj = models.PricePolicy.objects.get(id=pk)
    if request.method == 'GET':
        form = PriceModelForm(instance=obj)
        return render(request, 'form.html', context={
            'form': form,
        })
    elif request.method == 'POST':
        form = PriceModelForm(instance=obj, data=request.POST)
        if not form.is_valid():
            return render(request, 'form.html', context={
                'form': form,
            })
        form.save()
        return redirect(reverse(viewname='price_edit'))


def price_delete(request, pk):
    # exist = models.Customer.objects.filter(prior_id=pk, active=1).select_related('prior').exists()
    # if exist:
    #     return BaseResponse(False, details='当前级别下存在用户，无法删除').as_json()
    models.PricePolicy.objects.filter(id=pk).update(active=0)
    return BaseResponse(True, details="").as_json()
