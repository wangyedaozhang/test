import math

from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views import View

from goodsapp.models import Category, Goods


class IndexView(View):
    def get(self,request, categoryid=2, num=1):
        categoryid = int(categoryid)

        # 1.获取所有的商品类别信息
        categoryList = Category.objects.all().order_by('id')

        # 2.获取某个类别下所有的商品信息
        goodsList = Goods.objects.filter(category_id = categoryid)

        # 3.添加分页功能
        paginatorObj = Paginator(object_list=goodsList, per_page=8)

        page_goods_obj = paginatorObj.page(num)
        start = num - math.ceil(10/2)

        if start < 1:
            start = 1
        end = start + 9

        if end > paginatorObj.num_pages:
            end = paginatorObj.num_pages

        if end < 10:
            start = 1

        else:
            start = end - 9

        page_list = range(start, end+1)


        return  render(request,'index.html', {'categoryList':categoryList,'goodsList':
            page_goods_obj,'currentCid':categoryid, 'page_list':page_list})


def recommend(func):
    def _wrapper(detailView,request, goodsid, *args, **kwargs):
        # 获取cookie中的goodsid字符串
        c_goodsid = request.COOKIES.get('c_goodsid','')

        # 存放用户访问过的商品ID列表
        goodsIdList = [id for id in c_goodsid.split() if id.strip()]

        # 存放用户访问过的商品对象列表
        goodsid = str(goodsid)
        goodsObjList = [Goods.objects.get(id=gid) for gid in goodsIdList if gid != goodsid and Goods.objects.get(id=gid).category_id == Goods.objects.get(id=goodsid).category_id][:4]

        if goodsid in goodsIdList:
            goodsIdList.remove(goodsid)
            goodsIdList.insert(0,goodsid)
        else:
            goodsIdList.insert(0,goodsid)

        # 调用视图方法
        response = func(detailView,request,goodsid,recommend_list=goodsObjList,*args,**kwargs)

        # 将用户访问过的商品ID列表存放至cookie中
        #' '.join(goodsIdList)
        a = [str(i) for i in goodsIdList]
        #" ".join('%s' %id for id in goodsIdlist)
        response.set_cookie('c_goodsid',' '.join(a),max_age=3*24*60*60)

        return response

    return _wrapper



class DetailView(View):
    @recommend
    def get(self,request,goodsid,recommend_list=[]):
        goodsid = str(goodsid)

        #根据商品ID或获取详情信息
        try:
            goods = Goods.objects.get(id=goodsid)
            return render(request, 'detail.html',{'goods':goods,'recommend_list':recommend_list})
        except Goods.DoesNotExist:
            return HttpResponse(status=404)