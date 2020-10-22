from django.db import models


# Create your models here.

class BuyerUser(models.Model):
    username = models.CharField(max_length=128)
    password = models.CharField(max_length=128)
    email = models.EmailField()
    phone = models.CharField(max_length=64)
    address = models.CharField(max_length=128)


class ShoppingCart(models.Model):
    goods_id = models.IntegerField()
    goods_name = models.CharField(max_length=128)
    goods_img = models.CharField(max_length=128)
    goods_price = models.DecimalField(max_digits=5, decimal_places=2)
    goods_num = models.IntegerField(default=20)
    store_id = models.IntegerField()
    buyer_user = models.ForeignKey(to=BuyerUser, on_delete=models.CASCADE)


class UserAddress(models.Model):
    receiver = models.CharField(max_length=64)
    detail_address = models.CharField(max_length=128)
    postcode = models.CharField(max_length=64)
    phone = models.CharField(max_length=32)
    status = models.BooleanField(default=False)
    buyer_user = models.ForeignKey(to=BuyerUser, on_delete=models.CASCADE)


class Orders(models.Model):
    order_numbering = models.CharField(max_length=128)
    order_date = models.DateTimeField()
    order_address = models.CharField(max_length=128)
    order_total = models.CharField(max_length=32)
    order_status = models.BooleanField(default=False)
    buyer_user = models.ForeignKey(to=BuyerUser, on_delete=models.CASCADE)


class OrdersDetail(models.Model):
    goods_name = models.CharField(max_length=128)
    goods_price = models.DecimalField(max_digits=6, decimal_places=2)
    goods_img = models.CharField(max_length=128)
    goods_num = models.IntegerField()
    goods_total = models.CharField(max_length=32)
    orders = models.ForeignKey(to=Orders, on_delete=models.CASCADE)


class CheckEmail(models.Model):
    email_address = models.CharField(max_length=64)
    ver_code = models.CharField(max_length=32)
    times = models.DateTimeField()
