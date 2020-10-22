from django.db import models


# Create your models here.

class Seller(models.Model):
    username = models.CharField(max_length=32, null=False)
    password = models.CharField(max_length=128, null=False)
    email = models.EmailField()
    phone = models.CharField(max_length=32)
    address = models.CharField(max_length=128)
    gender = models.BooleanField(default=True)
    header_img = models.ImageField(upload_to='img')


class Store(models.Model):
    name = models.CharField(max_length=128, null=False)
    address = models.CharField(max_length=128)
    desc = models.CharField(max_length=128)
    logo = models.ImageField(upload_to='img')

    seller = models.OneToOneField(to=Seller, on_delete=models.CASCADE)


class GoodsType(models.Model):
    name = models.CharField(max_length=128)
    logo = models.ImageField(upload_to='img')


class Goods(models.Model):
    name = models.CharField(max_length=128)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    shelf_life = models.CharField(max_length=128)
    production_date = models.DateField()
    desc = models.CharField(max_length=128)
    detail = models.TextField(default="商品详情")
    images = models.ImageField(upload_to='img')
    goodstype = models.ForeignKey(to=GoodsType, on_delete=models.CASCADE)
    level = models.IntegerField(default=0)
    store = models.ForeignKey(to=Store, on_delete=models.CASCADE, null=True, blank=True)
