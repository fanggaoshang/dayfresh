from django.urls import path
from seller import views

urlpatterns = [
    path('index/', views.index),
    path('store/', views.store),

    path('register/', views.register),
    path('login/', views.login),
    path('logout/', views.logout),

    path('goodstype_list/', views.goodstype_list),
    path('add_goodstype/', views.add_goodstype),
    path('edit_goodstype/', views.edit_goodstype),
    path('delete_goodstype/', views.delete_goodstype),

    path('add_goods/', views.add_goods),
    path('goods_list/', views.goods_list),
    path('goods_count/', views.goods_count),

    path('orders_count/', views.orders_count),
    path('orders_status/', views.orders_status),
]
