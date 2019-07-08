import hashlib
from random import randint


from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from App.models import User, Goods, Category, Perfume, Snacks, Brand, Collect, Shoppingcart
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
    # 取出用户的购物车中商品
    if username:
        user = User.objects.get(username=username)
        shopping = user.shoppingcart_set.all()
        for goods in shopping:
            picture = goods.goods.picture_set.filter(main=0).first().url
            goods.picture = picture
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
    request.session["yzm"] = yzm
    email = request.POST.get("email")
    send_mail('尤洪注册用户验证码', content, settings.EMAIL_FROM, [email], fail_silently=False)
    return JsonResponse({"yzm":yzm})


def member(request):
    username = request.session.get("username")
    user = User.objects.get(username=username)
    return render(request, "app/Member.html", context={"user":user})


def memberaddress(request):
    return render(request, "app/Member_Address.html")


def memberorder(request):
    return render(request, "app/Member_Order.html")


def membercollect(request):
    return render(request, "app/Member_Collect.html")


def membersafe(request):
    return render(request, "app/Member_Safe.html")


def getpassword(request):
    if request.method == "POST":
        form = GetpasswordForm(request.POST)
        if request.session.get("yzm"):
            del request.session["yzm"]
        if form.is_valid():
            username = form.cleaned_data["username"]
            print(username)
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
    # 取出用户的购物车中商品
    if username:
        user = User.objects.get(username=username)
        shopping = user.shoppingcart_set.all()
        for goods in shopping:
            picture = goods.goods.picture_set.filter(main=0).first().url
            goods.picture = picture
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
    })


def product(request, gid):
    category_one = Category.objects.filter(classgrade=1)
    category_two = Category.objects.filter(classgrade=2)
    category_three = Category.objects.filter(classgrade=3)
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
    })


@csrf_exempt
def docollect(request):
    if request.method == "POST":
        gid = request.POST.get("id")
        username = request.session.get("username")
        user = User.objects.get(username=username)
        goods = Goods.objects.get(pk=gid)
        Collect.objects.create(user=user, goods=goods)
    return JsonResponse({"ok":1})


@csrf_exempt
def doshopping(request):
    if request.method == "POST":
        gid = request.POST.get("id")
        print(gid)
        count = request.POST.get("count")
        username = request.session.get("username")
        user = User.objects.get(username=username)
        goods = Goods.objects.get(pk=gid)
        print(goods)
        print("*******************")
        price = request.POST.get("price")
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
    return render(request,"app/BuyCar.html", context={
        "category_one": category_one,
        "category_two": category_two,
        "category_three": category_three,
        "shopping": shopping,

    })


def buycartwo(request):
    return render(request, "app/BuyCar_Two.html")