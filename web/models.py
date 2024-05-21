from django.db import models


# Create your models here.
class ActiveBaseModel(models.Model):
    active = models.SmallIntegerField(verbose_name="状态", choices=(('1', '激活'), ('2', '删除')), default=1)

    class Meta:
        abstract = True


class Administrator(ActiveBaseModel):
    # 管理员
    username = models.CharField(verbose_name="用户名", max_length=15, unique=True)
    password = models.CharField(verbose_name="密码", max_length=255)
    phone = models.CharField(verbose_name="手机号", max_length=13)
    email = models.EmailField(verbose_name='电子邮箱', unique=True, null=True, blank=True)
    create_datetime = models.DateTimeField(verbose_name="创建日期", auto_now_add=True)


class Customer(ActiveBaseModel):
    # 顾客
    username = models.CharField(verbose_name="用户名", max_length=15, unique=True)
    password = models.CharField(verbose_name="密码", max_length=255)
    phone = models.CharField(verbose_name="手机号", max_length=13)
    email = models.EmailField(verbose_name='电子邮箱', unique=True, null=True, blank=True)
    creator = models.ForeignKey(verbose_name="创建者", to="Administrator", on_delete=models.CASCADE,
                                limit_choices_to={'active': 1})
    balance = models.DecimalField(verbose_name="余额", max_digits=10, decimal_places=2, default=0)

    prior = models.ForeignKey(verbose_name="等级", to="Prior", on_delete=models.CASCADE,
                              limit_choices_to={'active': 1})

    create_datetime = models.DateTimeField(verbose_name="创建日期", auto_now_add=True)


class Prior(ActiveBaseModel):
    # 用户等级折扣特权
    def __str__(self):
        return self.title

    title = models.CharField(verbose_name="等级头衔", max_length=20)
    discount = models.SmallIntegerField(verbose_name="折扣值")


class PricePolicy(ActiveBaseModel):
    # 播放量数量和价格对应规则
    count = models.IntegerField(verbose_name="增加播放量")
    price = models.DecimalField(verbose_name="价格", max_digits=10, decimal_places=2, default=0)


class Order(ActiveBaseModel):
    # 订单
    status_choices = ((1, "待执行"), (2, "正在执行"), (3, "已完成"), (4, "失败"), (5, "已撤单"))
    status = models.SmallIntegerField(verbose_name="订单状态", choices=status_choices, default=1)

    oid = models.CharField(verbose_name="订单号", max_length=20)
    url = models.CharField(verbose_name="视频地址", max_length=1024)
    count = models.IntegerField(verbose_name="播放量")
    origin_view_count = models.CharField(verbose_name="视频原播放量", max_length=32, default=0)
    price = models.DecimalField(verbose_name="费用", max_digits=10, decimal_places=2)
    real_price = models.DecimalField(verbose_name="实际收费", max_digits=10, decimal_places=2)

    create_datetime = models.DateTimeField(verbose_name="创建日期", auto_now_add=True)
    customer = models.ForeignKey(verbose_name="订单客户", to="Customer", on_delete=models.CASCADE)
    memo = models.TextField(verbose_name="备注", null=True, blank=True)


class TransactionRecord(ActiveBaseModel):
    # 交易记录
    charge_type_mapping = {
        1: "success",
        2: "warning",
        3: "info",
        4: "danger",
        5: "dark",
    }
    # type可能是（1.充值，2.扣费，3.下单，4.撤单，5.删除订单）
    charge_type_choices = ((1, "充值"),
                           (2, "扣款"),
                           (3, "下单"),
                           (4, "删单"),
                           (5, "撤单"))
    charge_type = models.SmallIntegerField(verbose_name="交易类型", choices=charge_type_choices)
    admin = models.ForeignKey(verbose_name="管理员", to="Administrator", on_delete=models.CASCADE, null=True, blank=True)
    customer = models.ForeignKey(verbose_name="客户", to="Customer", on_delete=models.CASCADE)
    amount = models.DecimalField(verbose_name="金额", max_digits=10, decimal_places=2)
    order_id = models.CharField(verbose_name="订单号", max_length=20, null=True)
    create_datetime = models.DateTimeField(verbose_name="创建日期", auto_now_add=True)
