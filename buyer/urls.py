from django.urls import path
from buyer import views

urlpatterns = [
    path('index/', views.index),
    path('vue_test/', views.vue_test),
    path('more_goods_list/', views.more_goods_list),
    # path('more_goods_list_ajx/', views.more_goods_list_ajx),
    path('goodsviews/', views.GoodsViews.as_view()),
    path('register/', views.register),
    path('login/', views.login),
    path('logout/', views.logout),
    path('goods_detail/', views.goods_detail),

    path('my_goodscar/', views.my_goodscar),
    path('add_cart/', views.add_cart),
    path('change_goodscar_num/', views.change_goodscar_num),
    path('delete_car/', views.delete_car),

    path('usercenter/', views.usercenter),
    path('add_address/', views.add_address),
    path('alert_address_status/', views.alert_address_status),
    path('edit_address/', views.edit_address),

    path('orders_list/', views.orders_list),
    path('my_orders/', views.my_orders),
    path('now_buy/', views.now_buy),

    path('alipay_test/', views.alipay_test),
    path('zfb/', views.zfb),
    path('update_orders_status/', views.update_orders_status),

    path('check_email/', views.check_email),
    path('register_email/', views.register_email),
    path('yzm_ajax/', views.yzm_ajax),

    path('sms_register/', views.sms_register),
    path('sms_ajax/', views.sms_ajax),
]
