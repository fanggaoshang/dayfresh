import os

from django.shortcuts import render, redirect
from seller.models import Seller, Store, GoodsType, Goods


# Create your views here.
# 主页
def index(request):
    return render(request, 'seller/index.html')


# ###################################################商品管理################################################
def goodstype_list(request):
    goodstype_obj_list = GoodsType.objects.all()
    return render(request, 'seller/goods_type_list.html', locals())


def add_goodstype(request):
    message = ""
    if request.method == "POST":
        goodstype_name = request.POST.get("goodstype_name")
        goodstype_img = request.FILES.get("goodstype_img")
        if all([goodstype_name, goodstype_img]):
            goodstype_obj = GoodsType(
                name=goodstype_name,
                logo=goodstype_img
            )
            goodstype_obj.save()
            return redirect("/seller/goodstype_list/")
        else:
            message = "信息不完整,请添加完整"
    return redirect("/seller/goodstype_list/")


def edit_goodstype(request):
    if request.method == "POST":
        goodstype_id = request.POST.get("id")
        goodstype_obj = GoodsType.objects.get(id=goodstype_id)
        goodstypename = request.POST.get("goodstypename")
        goodstypeimg = request.FILES.get("goodstypeimg")
        if goodstypeimg:
            path = 'static/' + goodstype_obj.logo.name
            os.remove(path)
            goodstype_obj.logo = goodstypeimg
        goodstype_obj.name = goodstypename
        goodstype_obj.save()
        return redirect('/seller/goodstype_list/')
    else:
        goodstype_id = request.GET.get("id")
        goodstype_obj = GoodsType.objects.get(id=goodstype_id)
        return render(request, 'seller/edit_goodstype.html', locals())


def delete_goodstype(request):
    goodstype_id = request.GET.get("id")
    goodstype_obj = GoodsType.objects.get(id=goodstype_id)
    path = 'static/' + goodstype_obj.logo.name
    os.remove(path)
    goods_obj_list = goodstype_obj.goods_set.all()
    for goods_obj in goods_obj_list:
        goods_img_path = 'static/' + goods_obj.images.name
        os.remove(goods_img_path)
    goodstype_obj.delete()
    return redirect('/seller/goodstype_list/')


def goods_list(request):
    seller_id = request.COOKIES.get("seller_id")
    store_obj = Store.objects.get(seller_id=seller_id)
    goods_obj_list = Goods.objects.filter(store_id=store_obj.id)
    return render(request, 'seller/goods_list.html', locals())


def add_goods(request):
    if request.method == "POST":
        name = request.POST.get("name")
        price = request.POST.get("price")
        bzq = request.POST.get("bzq")
        level = request.POST.get("level")
        productdate = request.POST.get("productdate")
        desc = request.POST.get("desc")
        detail = request.POST.get("detail")
        goodsimg = request.FILES.get("goodsimg")
        goodstype_id = request.POST.get("goodstype_id")

        seller_id = request.COOKIES.get("seller_id")
        store_id = Seller.objects.get(id=seller_id).store.id
        if all([name, price, bzq, productdate, goodsimg]):
            goods_obj = Goods(
                name=name,
                price=price,
                shelf_life=bzq,
                production_date=productdate,
                desc=desc,
                detail=detail,
                images=goodsimg,
                goodstype_id=goodstype_id,
                level=level,
                store_id=store_id
            )
            goods_obj.save()
            return redirect("/seller/goods_list/")
    else:
        goodstype_obj_list = GoodsType.objects.all()
    return render(request, 'seller/add_goods.html', locals())


def goods_count(request):
    return render(request, 'seller/goods_count.html')


# ###################################################订单管理################################################
def orders_status(request):
    return render(request, 'seller/orders_status.html')


def orders_count(request):
    return render(request, 'seller/orders_count.html')


# ####################################################店铺管理###############################################
def store(request):
    seller_id = request.COOKIES.get("seller_id")
    if request.method == "POST":
        store_id = request.POST.get("id")
        if store_id:
            '''修改店铺'''
            shopname = request.POST.get("shopname")
            shopaddress = request.POST.get("shopaddress")
            shopdesc = request.POST.get("shopdesc")
            shopimg = request.FILES.get("shopimg")
            store_obj = Store.objects.get(id=store_id)
            if shopimg:
                '''如果图片存在,想要替换图片,先把之前的删除'''
                path = 'static/' + store_obj.logo.name
                os.remove(path)
                store_obj.logo = shopimg
            store_obj.name = shopname
            store_obj.address = shopaddress
            store_obj.desc = shopdesc
            store_obj.save()
        else:
            shopname = request.POST.get("shopname")
            shopaddress = request.POST.get("shopaddress")
            shopdesc = request.POST.get("shopdesc")
            shopimg = request.FILES.get("shopimg")
            seller_id = request.COOKIES.get("seller_id")

            seller_obj = Seller.objects.get(id=seller_id)
            if all([shopname, shopaddress, shopdesc]):
                store_obj = Store(
                    name=shopname,
                    address=shopaddress,
                    desc=shopdesc,
                    logo=shopimg,
                    seller=seller_obj
                )
                store_obj.save()
        return redirect('/seller/index/')
    else:
        seller_id = request.COOKIES.get("seller_id")
        seller_obj = Seller.objects.get(id=seller_id)
        try:
            store_obj = seller_obj.store
        except:
            pass
        return render(request, 'seller/store.html', locals())


# #############################################注册登录退出##################################
def login(request):
    message = ''
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        seller_obj = Seller.objects.filter(username=username, password=password).first()
        if seller_obj:
            response = redirect('/seller/index')
            response.set_cookie('username', username)
            response.set_cookie('headimg', seller_obj.header_img)
            response.set_cookie('seller_id', seller_obj.id)
            return response
        else:
            message = "账号或密码错误"
    return render(request, 'seller/login.html', {"message": message})


def register(request):
    message = ""
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        address = request.POST.get("address")
        headimg = request.FILES.get("headimg")
        if all([username, password, email, phone, address]):
            seller_obj = Seller(
                username=username,
                password=password,
                email=email,
                phone=phone,
                address=address,
                header_img=headimg
            )
            seller_obj.save()
            return redirect('/seller/login/')
        else:
            message = '信息输入不完整,请重新输入'
    return render(request, 'seller/register.html', {"message": message})


def logout(request):
    response = redirect('/seller/login/')
    response.delete_cookie("username")
    response.delete_cookie("headimg")
    response.delete_cookie("seller_id")
    return response



