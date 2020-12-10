from django.http import HttpResponseRedirect


# Create your views here.
from django.shortcuts import render
from django.views import View

from cartapp.cartmanager import getCartManger


class CartView(View):
    def post(self,request):

        # 在session中存取数据时使用到多级字典时需要实时更新
        request.session.modified = True

        #获取用户当前操作类型
        flag = request.POST.get('flag','')

        if flag == 'add':
            cartManagerObj = getCartManger(request)
            cartManagerObj.add(**request.POST.dict())

        elif flag == 'plus':
            carttManagerObj = getCartManger(request)
            # {'flag':'plus','goodsid':'1'....}
            carttManagerObj.update(step=1, **request.POST.dict())

        elif flag == 'minus':
            cartManagetObj = getCartManger((request))
            cartManagetObj.update(step=-1, **request.POST.dict())

        elif flag == 'delete':
            cartManagetObj = getCartManger((request))
            cartManagetObj.delete(**request.POST.dict())

        return HttpResponseRedirect('/cart/queryAll/')


class CartListView(View):
    def get(self,request):

        #获取cartManager对象
        cartManagerObj = getCartManger(request)
        cartItemList = cartManagerObj.queryAll()

        return render(request,'cart.html',{'cartItemList':cartItemList})