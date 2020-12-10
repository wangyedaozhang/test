from django.db import models

# Create your models here.
from goodsapp.models import Color, Size, Goods
from userapp.models import UserInfo


class CartItem(models.Model):
    goodsid = models.PositiveIntegerField()
    colorid = models.PositiveIntegerField()
    sizeid = models.PositiveIntegerField()
    count = models.PositiveIntegerField(default=0)
    isdelete = models.BooleanField(default=False)
    user = models.ForeignKey(UserInfo, on_delete=models.DO_NOTHING)

    def getColor(self):
        return Color.objects.get(id=self.colorid)

    def getSize(self):
        return Size.objects.get(id=self.sizeid)

    def getGoods(self):
        return Goods.objects.get(id=self.goodsid)

    def getTotalPrice(self):
        return int(self.getGoods().price)*int(self.count)