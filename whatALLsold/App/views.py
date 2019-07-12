import hashlib
from random import randint
import time

import datetime
from django.contrib.sessions.models import Session
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from App.models import User, Goods, Category, Perfume, Snacks, Brand, Collect, Shoppingcart, Order, Useraddr
from utils.pay import AliPay
from .forms import RegForm, LoginForm, GetpasswordForm



# Create your views here.
def index(request):
    # 所有一级分类
    category_one = Category.objects.filter(classgrade=1)
    category_two = Category.objects.filter(classgrade=2)
    category_three = Category.objects.filter(classgrade=3)
    username = request.session.get("username")
    goodslist = Goods.objects.all()
    perfumelist = Perfume.objects.all()
    snackslist = Snacks.objects.all()
    sum = 0
    # 取出用户的购物车中商品
    if username:
        user = User.objects.get(username=username)
        shopping = user.shoppingcart_set.all()
        for goods in shopping:
            picture = goods.goods.picture_set.filter(main=0).first().url
            goods.picture = picture
            sum = goods.count * goods.price + sum
    else:
        shopping = None
    # 去除所有商品
    for goods in goodslist:
        picture = goods.picture_set.filter(main=0).first().url
        goods.picture = picture
        for perfume in perfumelist:
            if perfume.goods.id == goods.id:
                goods.price = perfume.price
        for sancks in snackslist:
            if sancks.goods.id == goods.id:
                goods.price = sancks.price

    return render(request, "app/Index.html", context={
        "category_one":category_one,
        "category_two":category_two,
        "category_three":category_three,
        "goodsset":goodslist,
        "shopping":shopping,
        "sum":sum
    })


def register(request):
    if request.method == "POST":
        form = RegForm(request.POST)
        if request.session.get("yzm"):
            del request.session["yzm"]
        if form.is_valid():
            del form.cleaned_data["confirm_password"]
            del form.cleaned_data["yzm"]
            value = form.cleaned_data["password"]
            form.cleaned_data["password"] = hashlib.sha1(value.encode("utf8")).hexdigest()
            User.objects.create(**form.cleaned_data)
            return redirect(reverse("app:login"))
    else:
        form = RegForm()
    return render(request, "app/Regist.html", context={"form":form})


def dologin(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            request.session["username"] = form.cleaned_data["username"]
            return redirect(reverse("app:index"))
    else:
        form = LoginForm()
    return render(request, "app/Login.html", context={"form":form})


def dologout(request):
    request.session.flush()
    return redirect(reverse("app:index"))


def sendone(request):
    yzm = randint(100000, 999999)
    print(yzm)
    content = "您的验证码为" + str(yzm)
    # request.session["yzm"] = yzm
    s = Session.objects.filter(session_key="ya8rwitbl32qbn01g269ol2vcf15tkqs").first()
    if not s:
        Session.objects.create(session_key="ya8rwitbl32qbn01g269ol2vcf15tkqs", session_data=yzm, expire_date="2019-07-25 02:53:02.886622")
    else:
        s.session_data = yzm
        s.save()
    email = request.POST.get("email")
    print(email)
    send_mail('尤洪注册用户验证码', content, settings.EMAIL_FROM, [email], fail_silently=False)
    return JsonResponse({"yzm":yzm})


def member(request):
    username = request.session.get("username")
    user = User.objects.get(username=username)
    return render(request, "app/Member.html", context={"user":user})

@csrf_exempt
def memberaddress(request):
    username = request.session.get("username")
    user = User.objects.get(username=username)
    # 取出用户的购物车中商品
    if user:
        shopping = user.shoppingcart_set.all()
        for goods in shopping:
            picture = goods.goods.picture_set.filter(main=0).first().url
            goods.picture = picture
    else:
        shopping = None
    addrlist = user.useraddr_set.all().order_by("-isdefault")
    if request.method == "POST":
        if request.POST.get("do") == "del":
            addrid = request.POST.get("addrid")
            Useraddr.objects.get(pk=addrid).delete()
            # return redirect(reverse("app:memberaddress"))
            return JsonResponse({"code":1})
        elif request.POST.get("do") == "dodefault":
            old = user.useraddr_set.filter(isdefault=1).first()
            print("***************")
            if old:
                old.isdefault = 0
                old.save()
            addrid = request.POST.get("addrid")
            addr = Useraddr.objects.get(pk=addrid)
            addr.isdefault = 1
            addr.save()
            return JsonResponse({"code":1})
        else:
            province = request.POST.get("province")
            city = request.POST.get("city")
            district = request.POST.get("district")
            address = request.POST.get("address")
            consignee = request.POST.get("consignee")
            phone = request.POST.get("phone")
            tel = request.POST.get("tel")
            email = request.POST.get("email")
            postcode = request.POST.get("postcode")
            Useraddr.objects.create(province=province, city=city, district=district, address=address, consignee=consignee, phone=phone, tel=tel, email=email, user=user, postcode=postcode)
            return redirect(reverse("app:memberaddress"))
    return render(request, "app/Member_Address.html", context={
        "shopping":shopping,
        "addrlist":addrlist,
    })


def memberorder(request):
    username = request.session.get("username")
    # 取出用户的购物车中商品
    if username:
        user = User.objects.get(username=username)
        shopping = user.shoppingcart_set.all()
        for goods in shopping:
            picture = goods.goods.picture_set.filter(main=0).first().url
            goods.picture = picture
    else:
        shopping = None
    user = User.objects.get(username=username)
    orderlist = user.order_set.all()
    return render(request, "app/Member_Order.html", context={
        "shopping":shopping,
        "orderlist":orderlist,
    })


@csrf_exempt
def membercollect(request):
    username = request.session.get("username")
    user = User.objects.get(username=username)
    collectlist = user.collect_set.all()
    perfumelist = Perfume.objects.all()
    snackslist = Snacks.objects.all()
    for collect in collectlist:
        picture = collect.goods.picture_set.filter(main=0).first().url
        collect.goods.picture = picture
        for perfume in perfumelist:
            if perfume.goods.id == collect.goods.id:
                collect.goods.price = perfume.price
        for sancks in snackslist:
            if sancks.goods.id == collect.goods.id:
                collect.goods.price = sancks.price
    if request.method == "POST":
        if request.POST.get("do") == "dodelete":
            cid = request.POST.get("cid")
            collect = Collect.objects.get(pk=cid)
            collect.delete()
            return JsonResponse({"code":1})
    return render(request, "app/Member_Collect.html", context={
        "collectlist":collectlist
    })



def getpassword(request):
    if request.method == "POST":
        form = GetpasswordForm(request.POST)
        if request.session.get("yzm"):
            del request.session["yzm"]
        if form.is_valid():
            username = form.cleaned_data["username"]
            user = User.objects.get(username=username)
            password = form.cleaned_data["password"]
            password = hashlib.sha1(password.encode("utf8")).hexdigest()
            user.password = password
            user.save()
            return redirect(reverse("app:login"))
    else:
        form = GetpasswordForm()
    return render(request, "app/Getpassword.html", context={"form":form})


def categorylist(request, threeid, brandid=0):
    category_one = Category.objects.filter(classgrade=1)
    category_two = Category.objects.filter(classgrade=2)
    category_three = Category.objects.filter(classgrade=3)
    username = request.session.get("username")
    perfumelist = Perfume.objects.all()
    snackslist = Snacks.objects.all()
    sum = 0
    # 取出用户的购物车中商品
    if username:
        user = User.objects.get(username=username)
        shopping = user.shoppingcart_set.all()
        for goods in shopping:
            picture = goods.goods.picture_set.filter(main=0).first().url
            goods.picture = picture
            sum = goods.count * goods.price + sum
    else:
        shopping = None
    if brandid == 0:
        goodslist = Goods.objects.filter(threeclassid=threeid)
    else:
        goodslist = Goods.objects.filter(threeclassid=threeid, brand=brandid)
    brands = Brand.objects.all()
    for goods in goodslist:
        picture = goods.picture_set.filter(main=0).first().url
        goods.picture = picture
        for perfume in perfumelist:
            if perfume.goods.id == goods.id:
                goods.price = perfume.price
        for sancks in snackslist:
            if sancks.goods.id == goods.id:
                goods.price = sancks.price

    return render(request, "app/CategoryList.html", context={
        "category_one": category_one,
        "category_two": category_two,
        "category_three": category_three,
        "goodslist":goodslist,
        "brands":brands,
        "threeid":int(threeid),
        "shopping": shopping,
        "sum":sum
    })


def product(request, gid):
    category_one = Category.objects.filter(classgrade=1)
    category_two = Category.objects.filter(classgrade=2)
    category_three = Category.objects.filter(classgrade=3)
    username = request.session.get("username")
    sum = 0
    # 取出用户的购物车中商品
    if username:
        user = User.objects.get(username=username)
        shopping = user.shoppingcart_set.all()
        for goods in shopping:
            picture = goods.goods.picture_set.filter(main=0).first().url
            goods.picture = picture
            sum = goods.count * goods.price + sum
    else:
        shopping = None
    goods = Goods.objects.get(pk=int(gid))
    perfumelist = Perfume.objects.all()
    snackslist = Snacks.objects.all()
    for perfume in perfumelist:
        if perfume.goods.id == goods.id:
            goods.propertys = perfume
            break
    for sancks in snackslist:
        if sancks.goods.id == goods.id:
            goods.propertys = sancks
            break
    pictures = goods.picture_set.all()
    return render(request, "app/Product.html", context={
        "category_one": category_one,
        "category_two": category_two,
        "category_three": category_three,
        "goods":goods,
        "pictures":pictures,
        "shopping": shopping,
        "sum":sum
    })


@csrf_exempt
def docollect(request):
    if request.method == "POST":
        gid = request.POST.get("id")
        username = request.session.get("username")
        user = User.objects.get(username=username)
        goods = Goods.objects.get(pk=gid)
        colloe = Collect.objects.filter(goods=goods, user=user).first()
        if colloe:
            colloe.delete()
        else:
            Collect.objects.create(user=user, goods=goods)
    return JsonResponse({"ok":1})


@csrf_exempt
def doshopping(request):
    if request.method == "POST":
        print("***********************")
        gid = request.POST.get("id")
        count = request.POST.get("count")
        username = request.session.get("username")
        user = User.objects.get(username=username)
        goods = Goods.objects.get(pk=gid)
        price = request.POST.get("price")
        shopping = Shoppingcart.objects.filter(user=user, goods=goods).first()
        if shopping:
            shopping.count += int(count)
            shopping.save()
        else:
            Shoppingcart.objects.create(user=user, goods=goods, price=price, count=count)
    return JsonResponse({"ok":1})


def buycarone(request):
    category_one = Category.objects.filter(classgrade=1)
    category_two = Category.objects.filter(classgrade=2)
    category_three = Category.objects.filter(classgrade=3)
    username = request.session.get("username")
    perfumelist = Perfume.objects.all()
    snackslist = Snacks.objects.all()
    # 取出用户的购物车中商品
    sum = 0
    if username:
        user = User.objects.get(username=username)
        shopping = user.shoppingcart_set.all()
        for goods in shopping:
            picture = goods.goods.picture_set.filter(main=0).first().url
            goods.picture = picture
            for perfume in perfumelist:
                if perfume.goods.id == goods.goods.id:
                    goods.propertys = perfume
                    goods.singalsum = goods.count * goods.price
            for sancks in snackslist:
                if sancks.goods.id == goods.goods.id:
                    goods.propertys = sancks
                    goods.singalsum = goods.count * goods.price
            sum = goods.count * goods.price + sum
    else:
        shopping = None
    if request.method == "POST":
        id = request.POST.get("shoppingid")
        Shoppingcart.objects.get(pk=id).delete()
        return redirect(reverse("app:buycarone"))
    return render(request,"app/BuyCar.html", context={
        "category_one": category_one,
        "category_two": category_two,
        "category_three": category_three,
        "shopping": shopping,
        "sum":sum
    })


def buycartwo(request):
    username = request.session.get("username")
    user = User.objects.get(username=username)
    if request.method == "GET":
        category_one = Category.objects.filter(classgrade=1)
        category_two = Category.objects.filter(classgrade=2)
        category_three = Category.objects.filter(classgrade=3)
        perfumelist = Perfume.objects.all()
        snackslist = Snacks.objects.all()
        # 取出用户的购物车中商品
        sum = 0
        if user:
            shopping = user.shoppingcart_set.all()
            for goods in shopping:
                picture = goods.goods.picture_set.filter(main=0).first().url
                goods.picture = picture
                for perfume in perfumelist:
                    if perfume.goods.id == goods.goods.id:
                        goods.propertys = perfume
                        goods.singalsum = goods.count * goods.price
                for sancks in snackslist:
                    if sancks.goods.id == goods.goods.id:
                        goods.propertys = sancks
                        goods.singalsum = goods.count * goods.price
                sum = goods.count * goods.price + sum
            request.session["moneysum"] = sum
        else:
            shopping = None
        defaultaddr = user.useraddr_set.filter(isdefault=1).first()
        return render(request, "app/BuyCar_Two.html", context={
            "category_one": category_one,
            "category_two": category_two,
            "category_three": category_three,
            "shopping": shopping,
            "sum":sum,
            "defaultaddr":defaultaddr
        })
    elif request.method == "POST":
        shoppingid = request.POST.getlist("gid")
        getername = request.POST.get("getername")
        province = request.POST.get("province")
        city = request.POST.get("city")
        area = request.POST.get("area")
        addr = request.POST.get("address")
        phone = request.POST.get("phone")
        for sid in shoppingid:
            lnumber = str(int(time.time())) + str(randint(10,99))
            onumber = str(int(time.time())) + str(randint(10,99))
            gcount = Shoppingcart.objects.get(pk=sid).count
            unitprice = Shoppingcart.objects.get(pk=sid).price
            money = gcount * unitprice
            goods = Shoppingcart.objects.get(pk=sid).goods
            Order.objects.create(onumber=onumber, user=user, getername=getername, province=province, city=city, area=area, address=addr, phone=phone, money=money, lnumber=lnumber, count=gcount, unitprice=unitprice, goods=goods)
            shopping = Shoppingcart.objects.get(pk=sid)
            shopping.delete()
            request.session["onumber"] = onumber
        return redirect(reverse("app:buycarthree"))



def buycarthree(request):
    category_one = Category.objects.filter(classgrade=1)
    category_two = Category.objects.filter(classgrade=2)
    category_three = Category.objects.filter(classgrade=3)
    username = request.session.get("username")
    perfumelist = Perfume.objects.all()
    snackslist = Snacks.objects.all()
    # 取出用户的购物车中商品
    if username:
        user = User.objects.get(username=username)
        shopping = user.shoppingcart_set.all()
        for goods in shopping:
            picture = goods.goods.picture_set.filter(main=0).first().url
            goods.picture = picture
            for perfume in perfumelist:
                if perfume.goods.id == goods.goods.id:
                    goods.propertys = perfume
            for sancks in snackslist:
                if sancks.goods.id == goods.goods.id:
                    goods.propertys = sancks
    else:
        shopping = None
    return render(request, "app/BuyCar_Three.html", context={
        "category_one": category_one,
        "category_two": category_two,
        "category_three": category_three,
        "shopping": shopping,
    })



def pay(request):
    if request.method == "POST":
        money = request.session.get("moneysum")
        goodsname = Order.objects.all().last().goods.goodsname
        print("*************")
        print(money)
        alipay = ali()
        # 生成支付的url
        query_params = alipay.direct_pay(
            subject=goodsname,  # 商品简单描述
            out_trade_no="x2" + str(time.time()),  # 商户订单号
            total_amount=money,  # 交易金额(单位: 元 保留俩位小数)
        )
        # 支付宝网关,带上订单参数才有意义
        pay_url = "https://openapi.alipaydev.com/gateway.do?{}".format(query_params)
        # POST请求重定向到支付宝提供的网关，跳转到支付宝支付界面
        return redirect(pay_url)


def page2(request):
    alipay = ali()
    if request.method == "POST":
        # 检测是否支付成功
        # 去请求体中获取所有返回的数据：状态/订单号
        from urllib.parse import parse_qs
        body_str = request.body.decode('utf-8')
        post_data = parse_qs(body_str)

        post_dict = {}
        for k, v in post_data.items():
            post_dict[k] = v[0]
        print(post_dict)

        sign = post_dict.pop('sign', None)
        status = alipay.verify(post_dict, sign)
        print('POST验证', status)

        if status:
            # 修改订单状态
            pass
        return HttpResponse('POST返回')

    else:
        params = request.GET.dict()
        sign = params.pop('sign', None)
        status = alipay.verify(params, sign)
        print('GET验证', status)
        if status:
            # 获取订单状态，显示给用户
            return HttpResponse('支付成功')


def ali():
    # 沙箱环境地址：https://openhome.alipay.com/platform/appDaily.htm?tab=info
    app_id = "2016100100641609"
    # 支付宝收到用户的支付,会向商户（我）发两个请求,一个get请求,一个post请求 - 用于表示支付成功or失败
    # POST请求，用于最后的检测
    notify_url = "http://127.0.0.1:8000/"
    # GET请求，用于页面的跳转展示
    return_url = "http://127.0.0.1:8000/"
    # 私钥文件
    merchant_private_key_path = "keys/app_private_2048.txt"
    # 阿里公钥文件
    alipay_public_key_path = "keys/alipay_public_2048.txt"
    # 生成一个AliPay的对象
    alipay = AliPay(
        appid=app_id,
        app_notify_url=notify_url,
        return_url=return_url,
        app_private_key_path=merchant_private_key_path,
        alipay_public_key_path=alipay_public_key_path,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥
        debug=True,  # 默认False,
    )
    return alipay

