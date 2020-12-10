from django.urls import path

from . import views

urlpatterns = [
    path('', views.toOrderView),
    path('toPay/', views.toPayView),
    path('checkPay/', views.checkPayView),
]