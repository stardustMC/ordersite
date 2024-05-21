from web import models
from django import forms
from utils.pager import PagerHtmlModel
from utils.group import CrcSearchGroup, Option, SearchGroupRow
from utils.response import BaseResponse
from utils.bootstrapform import BootStrapForm
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect, reverse


class CustomerTransRecordModelForm(BootStrapForm, forms.ModelForm):
    charge_type = forms.TypedChoiceField(label="交易类型", choices=((1, "充值"), (2, "扣费")), coerce=int)

    class Meta:
        model = models.TransactionRecord
        fields = ['charge_type', 'amount']

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount <= 0:
            raise ValidationError("金额数目必须大于0")
        return amount


def customer_charge(request, pk):
    if request.method == 'GET':
        # 第一步：配置和传参
        search_group = CrcSearchGroup(
            request,
            models.TransactionRecord,
            Option('charge_type'),  # choice
        )
        queryset = (models.TransactionRecord.objects.filter(customer_id=pk, customer__active=1, active=1)
                    .filter(**search_group.get_condition).select_related('customer').all().order_by('-id'))
        pager = PagerHtmlModel(request, queryset, 10)
        form = CustomerTransRecordModelForm()
        return render(request, 'customer_charge.html', context={
            'pager': pager,
            'customer_id': pk,
            'form': form,
            'search_group': search_group,
        })
    elif request.method == 'POST':
        pass


def customer_charge_add(request, pk):
    form = CustomerTransRecordModelForm(data=request.POST)
    if not form.is_valid():
        return BaseResponse(False, details=form.errors).as_json()

    from django.db import transaction
    try:
        with transaction.atomic():
            customer_obj = models.Customer.objects.filter(id=pk, active=1).select_for_update().first()
            amount = form.cleaned_data['amount']
            charge_type = form.cleaned_data['charge_type']

            if charge_type == 1:
                customer_obj.balance += amount
            elif charge_type == 2:
                if customer_obj.balance < amount:
                    form.add_error('__all__', "扣款金额不能大于余额")
                    return BaseResponse(False, details=form.errors).as_json()
                customer_obj.balance -= amount
            customer_obj.save()

            form.instance.customer = customer_obj
            form.save()
            return BaseResponse(True, "").as_json()
    except Exception as e:
        return BaseResponse(False, details={'__all__': ['操作失败']}).as_json()

