from django.urls import path

from . import views

urlpatterns = [
    path('',views.IndexView.as_view()),
    path('category/<int:categoryid>/',views.IndexView.as_view()),
    path('category/<int:categoryid>/page/<int:num>',views.IndexView.as_view()),
    path('goodsdetails/<int:goodsid>/',views.DetailView.as_view()),
]