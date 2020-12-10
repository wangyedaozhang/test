from django.db import models

# Create your models here.


class Category(models.Model):
    cname = models.CharField(max_length=10)

    def __str__(self):
        return self.cname


class Goods(models.Model):
    gname = models.CharField(verbose_name='商品名称', max_length=100)
    gdesc = models.CharField(verbose_name='商品描述', max_length=100)
    oldprice = models.DecimalField(verbose_name='原价', max_digits=5, decimal_places=2)
    price = models.DecimalField(verbose_name='现价', max_digits=5, decimal_places=2)
    category = models.ForeignKey(Category,on_delete=models.CASCADE, verbose_name='类别ID', )

    def __str__(self):
        return self.gname

    def getImgUrl(self):
        return self.inventory_set.first().color.colorurl

    def getColors(self):
        colors = []

        for inventory in self.inventory_set.all():
            color = inventory.color
            if color not in colors:
                colors.append(color)
        return colors

    def getSizes(self):
        sizes = []

        for inventory in self.inventory_set.all():
            size = inventory.size
            if size not in sizes:
                sizes.append(size)
        return sizes


    # {'参数规格'：['ul'],'整体款式'：'url', '模特实拍':'[url]'}
    def getDetaiInfo(self):
        datas = {}

        for detail in self.goodsdetail_set.all():
            # 获取详情名称
            detailName = detail.getDName()
            # 判断detailname是否在字典中存在
            if detailName not in datas:
                datas[detailName] = [detail.gdurl]
            else:
                datas[detailName].append(detail.gdurl)

        return datas


class GoodsDetailName(models.Model):
    gdname = models.CharField(verbose_name='详情名称', max_length=30)

    def __str__(self):
        return self.gdname


class GoodsDetail(models.Model):
    gdurl = models.ImageField(verbose_name='详情图片地址', upload_to='')
    detailname = models.ForeignKey(GoodsDetailName, on_delete=models.DO_NOTHING)
    goods = models.ForeignKey(Goods, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.detailname.gdname

    def getDName(self):
        return self.detailname.gdname


class Size(models.Model):
    sname = models.CharField(verbose_name='尺寸名称', max_length=10)

    def __str__(self):
        return self.sname


class Color(models.Model):
    colorname = models.CharField(verbose_name='颜色名称', max_length=10)
    colorurl = models.ImageField(verbose_name='颜色图片地址', upload_to='color/')

    def __str__(self):
        return self.colorname


class Inventory(models.Model):
    count = models.PositiveIntegerField(verbose_name='库存数量')
    color = models.ForeignKey(Color, on_delete=models.DO_NOTHING)
    goods = models.ForeignKey(Goods, on_delete=models.DO_NOTHING)
    size = models.ForeignKey(Size, on_delete=models.DO_NOTHING)
