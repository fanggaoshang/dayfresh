import datetime
import random

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives

from buyer.models import BuyerUser, ShoppingCart, UserAddress, Orders, OrdersDetail, CheckEmail
from seller.models import GoodsType, Goods


def check_email(request):
    email_content = EmailMultiAlternatives(
        subject='hello jack',
        body='How are you?',
        from_email="fangyingdon@163.com",
        to=["786914141@qq.com"]
    )
    email_content.send()
    return HttpResponse("kfdowjfiow")


def register_email(request):
    dic = {'email_name_error': '', 'code_error': '', 'code_time_out': ''}
    if request.method == "POST":
        emailname = request.POST.get("emailname")
        code = request.POST.get("code")
        userpass = request.POST.get("userpass")
        email_obj = CheckEmail.objects.filter(email_address=emailname).first()
        if email_obj:
            if email_obj.ver_code == code:
                start_time = email_obj.times
                end_time = datetime.datetime.now()
                if (end_time - start_time).seconds < 120:
                    user_obj = BuyerUser(
                        username=emailname,
                        email=emailname,
                        password=userpass
                    )
                    user_obj.save()
                    email_obj.delete()
                    return redirect("/buyer/login/")
                else:
                    dic["code_time_out"] = "验证码已过期"
                    email_obj.delete()
            else:
                dic["code_error"] = "验证码输入有误"
        else:
            dic['email_name_error'] = '获取验证码邮箱和当前邮箱不一致'

    return render(request, 'buyer/register_email.html', locals())


def yzm_ajax(request):
    dic = {"status": "ok", "data": ''}
    email_address = request.GET.get("email")
    if email_address:
        verification_code = str(random.randint(1000, 9999))
        try:
            mail_content = EmailMultiAlternatives(
                subject='天天生鲜验证码',
                body="您当前注册的验证码为：" + verification_code + "，请与两分钟内输入完成验证。",
                from_email="fangyingdon@163.com",
                to=[email_address]
            )
            mail_content.send()
        except:
            dic["data"] = "请检查邮箱是否正确！"
            dic["status"] = "error"
            print('错误L ....')
        else:
            user_obj = BuyerUser.objects.filter(email=email_address).first()
            if user_obj:
                dic["data"] = "邮箱已存在！"
                dic["status"] = "error"
            else:
                check_email_obj = CheckEmail(
                    email_address=email_address,
                    ver_code=verification_code,
                    times=datetime.datetime.now()
                )
                check_email_obj.save()

    else:
        dic["data"] = "请检查邮箱是否正确！"
        dic["status"] = "error"
    return JsonResponse(dic)


def sms_register(request):
    sms_dic = {'email_name_error': '', 'code_error': '', 'code_time_out': ''}
    if request.method == "POST":
        phone_num = request.POST.get("phone_num")
        code = request.POST.get("code")
        userpass = request.POST.get("userpass")
        email_obj = CheckEmail.objects.filter(email_address=phone_num).first()
        if email_obj:
            if email_obj.ver_code == code:
                start_time = email_obj.times
                end_time = datetime.datetime.now()
                if (end_time - start_time).seconds < 120:
                    user_obj = BuyerUser(
                        username=phone_num,
                        email=phone_num,
                        password=userpass
                    )
                    user_obj.save()
                    email_obj.delete()
                    return redirect("/buyer/login/")
                else:
                    sms_dic["code_time_out"] = "验证码已过期"
                    email_obj.delete()
            else:
                sms_dic["code_error"] = "验证码输入有误"
        else:
            sms_dic['email_name_error'] = '获取验证码手机号和当前手机号不一致'
    return render(request, 'buyer/register_email22.html')


def send_sms(phone, ver_code):
    from ronglian_sms_sdk import SmsSDK

    accId = "8a216da8751c49c701753e68b1110a4f"
    accToken = "df298cfeb3084a1ab89b14ebcb5bdece"
    appId = "8a216da8751c49c701753e68b2700a56"
    sdk = SmsSDK(accId, accToken, appId)
    ret = sdk.sendMessage(tid='1', mobile=phone, datas=(ver_code, '2'))
    return ret


def sms_ajax(request):
    sms_dict = {"status": "success", "data": ''}
    phone_num = request.GET.get("phone_num")
    if phone_num:
        verification_code = str(random.randint(1000, 9999))
        try:
            ret = send_sms(phone_num, verification_code)
            if ret["statusCode"] != "000000":
                raise
        except:
            sms_dict["data"] = "请检查手机号是否正确！"
            sms_dict["status"] = "error"
        else:
            user_obj = BuyerUser.objects.filter(email=phone_num).first()
            if user_obj:
                sms_dict["data"] = "手机号已存在！"
                sms_dict["status"] = "error"
            else:
                check_email_obj = CheckEmail(
                    email_address=phone_num,
                    ver_code=verification_code,
                    times=datetime.datetime.now()
                )
                check_email_obj.save()

    else:
        sms_dict["data"] = "请检查手机号是否正确！"
        sms_dict["status"] = "error"
    return JsonResponse(sms_dict)


# #################################################首页###############################################
def index(request):
    goodstype_obj_list = GoodsType.objects.all()
    lb_goods_obj_list = Goods.objects.filter(level=1)
    advertising_list = Goods.objects.filter(level=2)
    return render(request, 'buyer/index(2).html', locals())


# 详情页面
def goods_detail(request):
    goods_id = request.GET.get("id")
    goods_obj = Goods.objects.get(id=goods_id)
    goodstype_id = goods_obj.goodstype_id
    goods_obj_list = Goods.objects.filter(level=0, goodstype_id=goodstype_id).order_by('-id')
    return render(request, 'buyer/detail.html', locals())


# 加入购物车
def add_cart(request):
    user_id = request.COOKIES.get("user_id")
    if user_id:
        goods_id = request.GET.get("goods_id")
        goods_num = request.GET.get("goods_num")
        cart_goods = ShoppingCart.objects.filter(goods_id=goods_id, buyer_user_id=user_id).first()
        if cart_goods:
            cart_goods.goods_num += int(goods_num)
            cart_goods.save()
        else:
            goods_obj = Goods.objects.get(id=goods_id)
            cart_goods_obj = ShoppingCart(
                goods_id=goods_id,
                goods_name=goods_obj.name,
                goods_num=goods_num,
                goods_img=goods_obj.images.name,
                goods_price=goods_obj.price,
                store_id=goods_obj.store.id,
                buyer_user_id=user_id
            )
            cart_goods_obj.save()
        dic = {"suc": "ok"}
    else:
        dic = {"suc": "false"}

    return JsonResponse(dic)


# 购物车页面
def my_goodscar(request):
    user_id = request.COOKIES.get("user_id")
    if user_id:
        user_id = request.COOKIES.get("user_id")
        cart_obj_list = ShoppingCart.objects.filter(buyer_user_id=user_id)
        car_dic_list = []
        for car_obj in cart_obj_list:
            dic = {}
            price = car_obj.goods_price
            number = car_obj.goods_num
            xiaoji = price * number
            dic['xiaoji'] = xiaoji
            dic['car_obj'] = car_obj
            car_dic_list.append(dic)
        return render(request, 'buyer/cart.html', locals())
    else:
        messages.warning(request, "请登录后查看购物车内商品")
        return render(request, 'buyer/cart.html')


# 订单列表和订单详情
def orders_list(request):
    user_id = request.COOKIES.get("user_id")
    print(request.method)
    if request.method == "POST":
        shoppingcarids = request.POST.getlist("shoppingcarids")
        print(shoppingcarids)
        times = datetime.datetime.now()
        time_num = times.strftime("%Y%m%d%H%M%S")
        order_obj = Orders()
        order_obj.order_numbering = time_num + str(random.randint(0, 9))
        order_obj.order_date = times
        user_address_obj = UserAddress.objects.filter(buyer_user_id=user_id, status=True).first()
        if user_address_obj:
            order_obj.order_address = user_address_obj.detail_address + ' (' + user_address_obj.receiver + ' 收)' + user_address_obj.phone
        else:
            order_obj.order_address = ''
        order_obj.order_total = ''
        order_obj.buyer_user_id = user_id
        order_obj.save()
        totals = 0
        for shoppingcarid in shoppingcarids:
            # 订单详情
            cart_obj = ShoppingCart.objects.filter(buyer_user_id=user_id, id=shoppingcarid).first()
            order_detail_obj = OrdersDetail(
                goods_name=cart_obj.goods_name,
                goods_price=cart_obj.goods_price,
                goods_num=cart_obj.goods_num,
                goods_img=cart_obj.goods_img,
                goods_total=cart_obj.goods_price * cart_obj.goods_num,
                orders=order_obj
            )
            order_detail_obj.save()
            print(cart_obj)
            totals += cart_obj.goods_price * cart_obj.goods_num
            cart_obj.delete()
        order_obj.order_total = totals
        order_obj.save()
        return render(request, 'buyer/place_order.html',
                      {"orders_obj": order_obj, "address_obj": user_address_obj})
    else:
        pass


# 改变购物车中商品的数量
def change_goodscar_num(request):
    user_id = request.COOKIES.get("user_id")
    shoppingcar_id = request.GET.get("shoppingcar_id")
    flag = request.GET.get("flag")
    print(shoppingcar_id, flag, user_id)
    cart_goods = ShoppingCart.objects.filter(id=shoppingcar_id, buyer_user_id=user_id).first()

    if flag == "+":
        cart_goods.goods_num += 1
        cart_goods.save()

    if flag == "-":
        cart_goods.goods_num -= 1
        cart_goods.save()
    dic = {"suc": "ok"}
    return JsonResponse(dic)


# 删除购物车中的物品
def delete_car(request):
    cart_id = request.GET.get("id")
    cart_obj = ShoppingCart.objects.get(id=cart_id)
    cart_obj.delete()
    return redirect('/buyer/my_goodscar')


# 用户中心
def usercenter(request):
    user_id = request.COOKIES.get('user_id')
    address_obj_list = UserAddress.objects.filter(buyer_user_id=user_id).order_by('-id')
    return render(request, "buyer/user-center-info.html", locals())


# 添加地址
def add_address(request):
    if request.method == "POST":
        user_id = request.COOKIES.get("user_id")
        receiver = request.POST.get("receiver")
        detail_address = request.POST.get("detail_address")
        postcode = request.POST.get("postcode")
        phone = request.POST.get("phone")
        address_obj_list = UserAddress.objects.filter(buyer_user_id=user_id)
        print(receiver, detail_address, postcode, phone)
        if address_obj_list:
            address_obj_list.update(status=False)
        user_address = UserAddress(
            receiver=receiver,
            detail_address=detail_address,
            postcode=postcode,
            phone=phone,
            status=True,
            buyer_user_id=user_id
        )
        user_address.save()
    return redirect("/buyer/usercenter/")


# 修改地址状态
def alert_address_status(request):
    dic = {"suc": "ok"}
    user_id = request.COOKIES.get("user_id")
    user_address_id = request.GET.get("user_address_id")
    UserAddress.objects.filter(buyer_user_id=user_id).update(status=False)
    user_address_obj = UserAddress.objects.filter(id=user_address_id).first()
    user_address_obj.status = True
    user_address_obj.save()
    return JsonResponse(dic)


# 编辑地址
def edit_address(request):
    if request.method == "POST":
        address_id = request.GET.get("id")
        user_id = request.COOKIES.get("user_id")
        receiver = request.POST.get("receiver")
        detail_address = request.POST.get("detail_address")
        postcode = request.POST.get("postcode")
        phone = request.POST.get("phone")
        if all([receiver, detail_address, postcode, phone]):
            address_obj = UserAddress.objects.get(id=address_id)
            address_obj.receiver = receiver
            address_obj.detail_address = detail_address
            address_obj.postcode = postcode
            address_obj.phone = phone
            address_obj.buyer_user_id = user_id
            address_obj.save()
            return redirect("/buyer/usercenter/")
        else:
            messages.warning(request, "信息不完整,请重新修改")
    address_obj_id = request.GET.get("id")
    address_obj = UserAddress.objects.get(id=address_obj_id)
    return render(request, 'buyer/edit-address.html', locals())


# 我的订单
def my_orders(request):
    user_id = request.COOKIES.get('user_id')
    orders_obj_list = Orders.objects.filter(buyer_user_id=user_id)
    for orders_obj in orders_obj_list:
        if not orders_obj.order_address:
            address_obj = UserAddress.objects.filter(status=True, buyer_user=user_id).first()
            orders_obj.order_address = address_obj.detail_address + ' (' + address_obj.receiver + " 收) " + address_obj.phone
            orders_obj.save()
    return render(request, 'buyer/myorders.html', locals())


def now_buy(request):
    user_id = request.COOKIES.get("user_id")
    goods_id = request.GET.get("goodsid")
    if user_id:
        goods_num = request.GET.get("number")
        times = datetime.datetime.now()
        time_num = times.strftime("%Y%m%d%H%M%S")
        order_obj = Orders()
        order_obj.order_numbering = time_num + str(random.randint(0, 9))
        order_obj.order_date = times
        user_address_obj = UserAddress.objects.filter(buyer_user_id=user_id, status=True).first()
        if user_address_obj:
            order_obj.order_address = user_address_obj.detail_address + ' (' + user_address_obj.receiver + ' 收)' + user_address_obj.phone
        else:
            order_obj.order_address = ''
        order_obj.order_total = ''
        order_obj.buyer_user_id = user_id
        order_obj.save()

        goods_obj = Goods.objects.get(id=goods_id)
        ordersdetail_obj = OrdersDetail(
            goods_name=goods_obj.name,
            goods_price=goods_obj.price,
            goods_img=goods_obj.images.name,
            goods_num=goods_num,
            goods_total=goods_obj.price * int(goods_num),
            orders=order_obj
        )
        ordersdetail_obj.save()
        order_obj.order_total = goods_obj.price * int(goods_num)
        order_obj.save()
        return render(request, 'buyer/place_order.html', {'orders_obj': order_obj, 'address_obj': user_address_obj})
    else:
        messages.warning(request, "请登录后购买")
        return redirect('/buyer/goods_detail/?id=' + goods_id)


from alipay import AliPay


# 支付宝
def alipay_test(request):
    # 个人私钥
    app_private_key_string = """-----BEGIN RSA PRIVATE KEY-----
    MIIEogIBAAKCAQEAm14zbrNRHqTl+M/QN/rZn4FYp7C2TnpLJouz4wc/5L8WidNrJQ+yrVvsS93ZcOri4/RkBWP8NEgbvDx6DDHTaKileY5ndSOFA89u/pd7Rwf0SYEbcrjR50bv51tVn1B3z2EzvwHeZrIJfSpkoB096SboFpEHYStN5BxBaTEjQbLAd4z7uVJmWVzuwhmKKYojghJNdUyyxJyrQwnQ2erHcGZ3mVDyW7nMo8sFd+KTvC8ZQBqXSUX6suHvUxfhyhOAWFDVtQQtJiUoX7cVswqpqgcMfRFfONcWodo/gd6GnQtBetaiwrGiXB84u4AqgAqHigQ3GX6j9G8DwbgV98GS4wIDAQABAoIBAExM+eM+qvLqton3vOERD3kW86v+y7lEs81tRF2VPNqgwXfUXUUpLW2XvDcR72xV3jFm3wwKq1wdoYlTBfkhKxq13/YPal2LoRJa976ONBuRG3ZRsmInw+XZ3412PFluEjjFGr2ONGOowaI3hI1hbvsmgUo71SzyMGF7QuBfIlproVi6Ce5F6KBa9XMy6USm+709WGuOAVwX1nQ9IlG0oimZjNS7/6tlli8rLIqrwqeu+wLjAaTsfo/PHugmaDyqRwEugAMEb+TrxeDE1A47rXA3ZNEy3XbwGeVFvWU7RnBLVUOJdTvWGbGpJZDGnb4ryzM2brbS9XREy8cGMWH14zkCgYEA6fMZVeu87ppEal7TI2KhDIU4qaj1+CnnFlHwGrhjjz7asjSFsCaiwwrs552JQbN/sirVw6wEvfI+W8cLC1w/h5QFp4Lpu/XIxFP0Q4wUKdm28cr0SPeoDOJRNQCEhXUgRHgYfeXgFgS6qK2FTgGN5TWqUKc5y5NVqAiu5QFgEDUCgYEAqgMHZW/Kl+sZxoIeKIxZ3d4+D97F1tknmzFrfX3f7Ho3VfSo3Lwfj0AbHkaVsmCcnBj/yBLUemrlrzeJRm3O2hu8cbB7J92uelQrM+4wcmdy0LoFvpxjUC2S9luk6wX41PKG12+TT9AvC9n9tGhUpXSTaIY4XwHU8ggA7H43qbcCgYAQ/8MFhT2TMM5r1DwPRCljmYKGgWpt/810x7tklaVWUUDe1gYoyIXnGjIgmkfQ6FQNBCPINgWaL7HsRUg+KRPMrCrFAzQsni1aZqdHCTSl3dX3N8IMU0J4vTEdYs4+TEZt8zQEYeGod+uAOiuHgYFn+EBJ3/zJGAmPTiI3LaRnSQKBgBm5M5lJfOHXlKLQdTe1ZLOJOOK11kFXwgJdS+JE9WiWZWEAD7y2SiAmlvPRwjynGYsUzT68eqG7It2MDZ02aCHgKHcbOMcjZ47ixVaqJ3Jn7JtgShY5G126R44295EH6kpuF7DpFOTynuuwJA7z6jrOlK8v/7+AS3QDegBOaKWpAoGATuAgk4cdH3CDbcPArwJVNenlqVtkPBFZFbso+o3Z4TZKxlOT5NSyffPr2PBQCgZZbGxERI4sF2ng12QltmDrr736a3zn3Wut6Qu0TCkGGpcWuo7rw1cFsJR3RvewNW2YMYobDpQqeiwG3fprl7sZ/3J4hV0Zbzpo4aW0Wc+i4A0=
    -----END RSA PRIVATE KEY-----"""
    # 支付宝公钥
    alipay_public_key_string = """-----BEGIN PUBLIC KEY-----
    MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAqvyu9SHhLfj24O2lZBpZw49eGHI4dUBl94GA0DWaRQBJGiseHpMrt3fMgH6ovFrkERYHbo0+fCGMG67vy9cLZ2huaM4TMYGgkpkqgLVPk3Dv2wfjBbXToCSw7W+oKZvBxSGlfvlBj/gaaHMf7rVMobk7rmhH5KJLZEiEt6bmuxJYOOSFKsyU3CK7GbJZx9JEu0vx02UpGzmykF5D+8YDcZOgLXFjRi+meejhsa/JNLbCkHe36ReBYzyXiZLgJL1hFbXOtOBzvXu2zNcOfA4aqz7oQVnzOJSFMEy2wPNOiC9oiqUjMlDyqKtAjPRL2PdEWzIt+TyECH8HgbYOmz08BQIDAQAB
    -----END PUBLIC KEY-----"""

    alipay = AliPay(
        appid="2021000116688388",
        app_notify_url=None,  # 默认回调url
        # 个人私钥
        app_private_key_string=app_private_key_string,
        # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
        alipay_public_key_string=alipay_public_key_string,
        sign_type="RSA2",  # RSA 或者 RSA2
        debug=False
    )

    # 电脑网站支付，需要跳转到https://openapi.alipaydev.com/gateway.do? + order_string
    order_string = alipay.api_alipay_trade_page_pay(
        out_trade_no="20161112",
        total_amount=str(2),
        subject="生鲜",
        return_url=None,
        notify_url=None  # 可选, 不填则使用默认notify url
    )
    url = "https://openapi.alipaydev.com/gateway.do?" + order_string
    return redirect(url)


def zfb(request):
    order_numbering = request.GET.get("orderno")
    order_total = request.GET.get("total")

    # 个人私钥
    app_private_key_string = """-----BEGIN RSA PRIVATE KEY-----
       MIIEogIBAAKCAQEAm14zbrNRHqTl+M/QN/rZn4FYp7C2TnpLJouz4wc/5L8WidNrJQ+yrVvsS93ZcOri4/RkBWP8NEgbvDx6DDHTaKileY5ndSOFA89u/pd7Rwf0SYEbcrjR50bv51tVn1B3z2EzvwHeZrIJfSpkoB096SboFpEHYStN5BxBaTEjQbLAd4z7uVJmWVzuwhmKKYojghJNdUyyxJyrQwnQ2erHcGZ3mVDyW7nMo8sFd+KTvC8ZQBqXSUX6suHvUxfhyhOAWFDVtQQtJiUoX7cVswqpqgcMfRFfONcWodo/gd6GnQtBetaiwrGiXB84u4AqgAqHigQ3GX6j9G8DwbgV98GS4wIDAQABAoIBAExM+eM+qvLqton3vOERD3kW86v+y7lEs81tRF2VPNqgwXfUXUUpLW2XvDcR72xV3jFm3wwKq1wdoYlTBfkhKxq13/YPal2LoRJa976ONBuRG3ZRsmInw+XZ3412PFluEjjFGr2ONGOowaI3hI1hbvsmgUo71SzyMGF7QuBfIlproVi6Ce5F6KBa9XMy6USm+709WGuOAVwX1nQ9IlG0oimZjNS7/6tlli8rLIqrwqeu+wLjAaTsfo/PHugmaDyqRwEugAMEb+TrxeDE1A47rXA3ZNEy3XbwGeVFvWU7RnBLVUOJdTvWGbGpJZDGnb4ryzM2brbS9XREy8cGMWH14zkCgYEA6fMZVeu87ppEal7TI2KhDIU4qaj1+CnnFlHwGrhjjz7asjSFsCaiwwrs552JQbN/sirVw6wEvfI+W8cLC1w/h5QFp4Lpu/XIxFP0Q4wUKdm28cr0SPeoDOJRNQCEhXUgRHgYfeXgFgS6qK2FTgGN5TWqUKc5y5NVqAiu5QFgEDUCgYEAqgMHZW/Kl+sZxoIeKIxZ3d4+D97F1tknmzFrfX3f7Ho3VfSo3Lwfj0AbHkaVsmCcnBj/yBLUemrlrzeJRm3O2hu8cbB7J92uelQrM+4wcmdy0LoFvpxjUC2S9luk6wX41PKG12+TT9AvC9n9tGhUpXSTaIY4XwHU8ggA7H43qbcCgYAQ/8MFhT2TMM5r1DwPRCljmYKGgWpt/810x7tklaVWUUDe1gYoyIXnGjIgmkfQ6FQNBCPINgWaL7HsRUg+KRPMrCrFAzQsni1aZqdHCTSl3dX3N8IMU0J4vTEdYs4+TEZt8zQEYeGod+uAOiuHgYFn+EBJ3/zJGAmPTiI3LaRnSQKBgBm5M5lJfOHXlKLQdTe1ZLOJOOK11kFXwgJdS+JE9WiWZWEAD7y2SiAmlvPRwjynGYsUzT68eqG7It2MDZ02aCHgKHcbOMcjZ47ixVaqJ3Jn7JtgShY5G126R44295EH6kpuF7DpFOTynuuwJA7z6jrOlK8v/7+AS3QDegBOaKWpAoGATuAgk4cdH3CDbcPArwJVNenlqVtkPBFZFbso+o3Z4TZKxlOT5NSyffPr2PBQCgZZbGxERI4sF2ng12QltmDrr736a3zn3Wut6Qu0TCkGGpcWuo7rw1cFsJR3RvewNW2YMYobDpQqeiwG3fprl7sZ/3J4hV0Zbzpo4aW0Wc+i4A0=
       -----END RSA PRIVATE KEY-----"""
    # 支付宝公钥
    alipay_public_key_string = """-----BEGIN PUBLIC KEY-----
       MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAqvyu9SHhLfj24O2lZBpZw49eGHI4dUBl94GA0DWaRQBJGiseHpMrt3fMgH6ovFrkERYHbo0+fCGMG67vy9cLZ2huaM4TMYGgkpkqgLVPk3Dv2wfjBbXToCSw7W+oKZvBxSGlfvlBj/gaaHMf7rVMobk7rmhH5KJLZEiEt6bmuxJYOOSFKsyU3CK7GbJZx9JEu0vx02UpGzmykF5D+8YDcZOgLXFjRi+meejhsa/JNLbCkHe36ReBYzyXiZLgJL1hFbXOtOBzvXu2zNcOfA4aqz7oQVnzOJSFMEy2wPNOiC9oiqUjMlDyqKtAjPRL2PdEWzIt+TyECH8HgbYOmz08BQIDAQAB
       -----END PUBLIC KEY-----"""

    alipay = AliPay(
        appid="2021000116688388",
        app_notify_url=None,  # 默认回调url
        # 个人私钥
        app_private_key_string=app_private_key_string,
        # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
        alipay_public_key_string=alipay_public_key_string,
        sign_type="RSA2",  # RSA 或者 RSA2
        debug=False
    )

    # 电脑网站支付，需要跳转到https://openapi.alipaydev.com/gateway.do? + order_string
    order_string = alipay.api_alipay_trade_page_pay(
        out_trade_no=order_numbering,
        total_amount=order_total,
        subject="生鲜",
        return_url="http://127.0.0.1:8000/buyer/update_orders_status/?orderno=" + order_numbering,
        notify_url=None  # 可选, 不填则使用默认notify url
    )
    url = "https://openapi.alipaydev.com/gateway.do?" + order_string
    return redirect(url)


def update_orders_status(request):
    orderno = request.GET.get('orderno')
    print(orderno)
    Orders.objects.filter(order_numbering=orderno).update(order_status=True)
    return redirect("/buyer/my_orders")


# ############################################查看更多###############################################
def more_goods_list(request):
    goodstype_id = request.GET.get("goodstype_id")
    goods_obj_list = Goods.objects.filter(level=0, goodstype_id=goodstype_id).order_by('-id')
    return render(request, 'buyer/list_v2.html', locals())


from rest_framework import generics
from .serializers import GoodsSerializers


class GoodsViews(generics.ListAPIView):
    def get_queryset(self):
        goodstype_id = self.request.GET.get("goodstype_id")
        goods_obj_list = Goods.objects.filter(goodstype_id=goodstype_id)
        return goods_obj_list

    serializer_class = GoodsSerializers

    def get_serializer_context(self):
        return {
            'view': self
        }


# ############################################登录注册退出登录##############################
def register(request):
    if request.method == "POST":
        user_name = request.POST.get("user_name")
        user_pwd = request.POST.get("user_pwd")
        user_email = request.POST.get("user_email")
        phone = request.POST.get("phone")
        address = request.POST.get("address")
        user_allow = request.POST.get("user_allow")
        buyer_user = BuyerUser(
            username=user_name,
            password=user_pwd,
            email=user_email,
            phone=phone,
            address=address
        )
        buyer_user.save()
        return redirect("/buyer/login")
    return render(request, "buyer/register.html")


def login(request):
    message = ""
    if request.method == "POST":
        user_name = request.POST.get("user_name")
        user_pwd = request.POST.get("user_pwd")
        user_obj = BuyerUser.objects.filter(username=user_name, password=user_pwd).first()
        if user_obj:
            response = redirect('/buyer/index')
            response.set_cookie('user_name', user_name)
            response.set_cookie('user_id', user_obj.id)
            return response
        else:
            message = '用户名或密码错误'
    return render(request, 'buyer/login.html', {"message": message})


def logout(request):
    response = redirect('/buyer/index')
    response.delete_cookie("user_name")
    response.delete_cookie("user_id")
    return response


# 测试vue
def vue_test(request):
    ip = request.META['REMOTE_ADDR']
    print(ip)
    return render(request, 'buyer/vue.html')
