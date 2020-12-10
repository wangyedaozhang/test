from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view()),
    path('center/', views.centerView),
    path('login/', views.LoginView.as_view()),
    path('loadCode/', views.LoadCodeView.as_view()),
    path('checkCode/', views.CheckCodeView.as_view()),
    path('logout/', views.LOgOutView.as_view()),
    path('address/', views.AddressView.as_view()),
    path('loadArea/', views.loadAreaView),
    path('updateDefaultAddr/', views.updateDefaultAddr),
]