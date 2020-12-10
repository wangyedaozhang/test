from django.db import models

# Create your models here.
from userapp.models import Address, UserInfo


class Order(models.Model):
    out_trade_num = models.UUIDField()
    order_num = models.CharField(max_length=50)
    trade_no = models.CharField(max_length=120,default='')
    status =models.CharField(max_length=20,default='待支付')
    payway = models.CharField(max_length=20,default='alipay')
    address = models.ForeignKey(Address,on_delete=models.DO_NOTHING)
    user= models.ForeignKey(UserInfo,on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.order_num


class OrderItem(models.Model):
    goodsid = models.PositiveIntegerField()
    colorid = models.PositiveIntegerField()
    sizeid = models.PositiveIntegerField()
    count = models.PositiveIntegerField()
    order = models.ForeignKey(Order,on_delete=models.DO_NOTHING)
