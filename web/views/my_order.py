import random
import datetime
from web import models
from django import forms
from django.db.models import Q, F
from django.db import transaction
from utils.pager import PagerHtmlModel
from utils.crawl import get_origin_view_count
from utils.response import BaseResponse
from utils.bootstrapform import BootStrapForm
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect, reverse


class OrderAddModelForm(BootStrapForm, forms.ModelForm):
    class Meta:
        model = models.Order
        fields = ['url', 'count', 'memo']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.unit_price_list = []
        queryset = models.PricePolicy.objects.order_by("count").all()
        for policy in queryset:
            self.unit_price_list.append([policy.count, policy.price / policy.count])
        self.fields['count'].help_text = ' '.join(["{}+ {}￥/条".format(count, unit_price)
                                                   for count, unit_price in self.unit_price_list])

    def clean_count(self):
        count = self.cleaned_data.get('count')
        min_count = self.unit_price_list[0][0]
        if count < min_count:
            raise ValidationError("播放量最低为{}".format(min_count))
        return count


def my_order(request):
    keyword = request.GET.get('keyword')
    con = Q()
    if keyword:
        con.connector = 'OR'
        con.children.append(('url__contains', keyword))
        con.children.append(('oid', keyword))
        for status, text in models.Order.status_choices:
            if keyword in text:
                con.connector = "AND"
                con.children.append(('status', status))
    queryset = models.Order.objects.filter(con).filter(active=1, customer_id=request.crc_user.id).all()
    pager = PagerHtmlModel(request, queryset, 10)
    print(pager)
    try:
        response = render(request, 'my_order.html', context={'pager': pager})
    except Exception as e:
        print(e)
        response = render(request, 'home.html')
    return response


def my_order_add(request):
    if request.method == 'GET':
        form = OrderAddModelForm()
        return render(request, 'form.html', context={'form': form})

    form = OrderAddModelForm(data=request.POST)
    if not form.is_valid():
        return render(request, 'form.html', context={'form': form})

    # crawl old video view count
    status, origin_view_count = get_origin_view_count(form.cleaned_data["url"])
    if not status:
        form.add_error('url', "视频地址无法解析,仅支持央视频")
        return render(request, 'form.html', context={'form': form})

    # calculate order price
    count = form.cleaned_data["count"]
    for i in range(len(form.unit_price_list) - 1, -1, -1):
        amount, unit_price = form.unit_price_list[i]
        if count >= amount:
            break

    # generate order id
    while True:
        cur_date = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        oid = cur_date + str(random.randint(10000, 99999))
        exist = models.Order.objects.filter(oid=oid).exists()
        if not exist:
            break

    with transaction.atomic():
        cus_obj = models.Customer.objects.filter(id=request.crc_user.id).select_for_update().first()
        # check if customer balance covers price
        origin_price = count * unit_price
        real_price = origin_price * cus_obj.prior.discount / 100
        if cus_obj.balance < real_price:
            form.add_error('count', "余额不足，当前订单需要{}￥".format(real_price))
            return render(request, 'form.html', context={'form': form})
        models.Customer.objects.filter(id=cus_obj.id).update(balance=F("balance") - real_price)
        # save Order form data
        form.instance.oid = oid
        form.instance.status = 1
        form.instance.customer = cus_obj
        form.instance.price = origin_price
        form.instance.real_price = real_price
        form.instance.origin_view_count = origin_view_count
        form.save()
        # create transaction record
        models.TransactionRecord.objects.create(
            charge_type=3,
            customer=cus_obj,
            amount=real_price,
            order_id=oid,
        )
        # push in redis queue
        from django.conf import settings
        from django_redis import get_redis_connection
        conn = get_redis_connection("default")
        conn.lpush(settings.REDIS_QUEUE_NAME, oid)
        return redirect(reverse(viewname='my_order'))


def my_order_revoke(request, pk):
    with transaction.atomic():
        order_obj = models.Order.objects.filter(id=pk, active=1, status=1).first()
        if not order_obj:
            if request.is_ajax():
                return BaseResponse(False, details="订单不存在或无法撤单").as_json()
            else:
                return redirect(reverse(viewname='my_order'))
        if order_obj.status != 1:
            if request.is_ajax():
                return BaseResponse(False, details="订单执行后无法撤销").as_json()
            else:
                return redirect(reverse(viewname='my_order'))

        record_obj = models.TransactionRecord.objects.filter(order_id=order_obj.oid, active=1).first()
        # step 1: return customer pay
        models.Customer.objects.filter(id=request.crc_user.id).update(balance=F("balance")+record_obj.amount)
        # step 2: nullify order status
        order_obj.status = 5
        order_obj.save()
        # step 3: create revoke record(instead of modifying the old one)
        models.TransactionRecord.objects.create(
            charge_type=5,
            customer_id=request.crc_user.id,
            amount=record_obj.amount,
            order_id=order_obj.oid,
        )
        if request.is_ajax():
            return BaseResponse(True, details="").as_json()
        else:
            return redirect(reverse(viewname='my_order'))
