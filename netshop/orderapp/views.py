import datetime
import uuid

import jsonpickle
from django.db.models import F
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from cartapp.cartmanager import DBCartManger
from goodsapp.models import Inventory
from orderapp.models import Order, OrderItem
from userapp.models import Address
from utils.alipay_p3 import AliPay


def toOrderView(request):
    cartitems = request.GET.get('cartitems', '')
    # 获取支付总金额
    totalPrice = request.GET.get('totalPrice', '')

    # 判断当前用户是否登录
    if not request.session.get('user', ''):
        # return HttpResponseRedirect('/user/login/?reflag=order&cartitems='+cartitems)
        return render(request, 'login.html', {'reflag': 'order', 'cartitems': cartitems})

    # 反序列化cartitems
    # [{'goodsid':1,'sizeid':'2','colorid':'3'},{}]
    cartitemList = jsonpickle.loads(cartitems)

    # 获取默认收货地址
    user = jsonpickle.loads(request.session.get('user', ''))
    addrObj = user.address_set.get(isdefault=True)

    # 获取订单内容
    # [CartItem(),CartItem()]
    cartItemObjList = [DBCartManger(user).get_cartitems(**item) for item in cartitemList if item]

    return render(request, 'order.html',
                  {'addrObj': addrObj, 'cartItemObjList': cartItemObjList, 'totalPrice': totalPrice})


alipayObj = AliPay(appid='2016110100785042', app_notify_url='http://127.0.0.1:8000/order/checkPay/', app_private_key_path='orderapp/keys/my_private_key.txt',
                 alipay_public_key_path='orderapp/keys/alipay_public_key.txt', return_url='http://127.0.0.1:8000/order/checkPay/', debug=True)

def toPayView(request):

    addrid = request.GET.get('address',-1)
    payway = request.GET.get('payway','alipay')
    cartitems = request.GET.get('cartitems','')

    params = {
        'out_trade_num': uuid.uuid4().hex,
        'order_num': datetime.datetime.now().strftime('%Y%m%d%H%M%S'),
        'address': Address.objects.get(id=addrid),
        'user': jsonpickle.loads(request.session.get('user','')),
        'payway': payway,
    }
    orderObj = Order.objects.create(**params)

    #'['{'goodsid:a','sizeid:2',....'}']'
    if cartitems:
        #[{dict1},{dict2}]
        cartitems = jsonpickle.loads(cartitems)

        orderItemList =[OrderItem.objects.create(order=orderObj,**ci) for ci in cartitems if ci]

    urlparam = alipayObj.direct_pay(subject='京东商城',out_trade_no=orderObj.out_trade_num,total_amount=request.GET.get('totalPrice',0))
    url = alipayObj.gateway+'?'+urlparam

    return HttpResponseRedirect(url)


def checkPayView(request):

    params = request.GET.dict()

    sign = params.pop('sign')

    if alipayObj.verify(params,sign):
        #
        user = jsonpickle.loads(request.session.get('user',''))
        #
        orderObj = Order.objects.get(out_trade_num=params.get('out_trade_no',''))
        orderObj.trade_no = params.get('trade_no','')
        orderObj.status = '待发货'
        orderObj.save()

        #
        orderItemList = orderObj.orderitem_set.all()
        [Inventory.objects.filter(goods_id=oi.goodsid,color_id=oi.colorid,size_id=oi.sizeid).update(count=F('count')-oi.count) for oi in orderItemList if oi]

        [user.cartitem_set.filter(goodsid=oi.goodsid,colorid=oi.colorid,sizeid=oi.sizeid).delete() for oi in orderItemList if oi]



        return HttpResponse('支付成功')
    return HttpResponse('支付失败')