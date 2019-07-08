import hashlib

import os
from datetime import datetime
from random import randint

from django.db import connection
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse

from App.models import *
from admin.forms import UserForm
from whatALLsold import settings


def login(request):
    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # password = hashlib.sha1(password.encode('utf-8')).hexdigest()
        res = User.objects.filter(username=username,password=password).values('username','id')
        print('*'*50)
        if len(res)>0:
            request.session['username']=res[0]['username']
            request.session['uid'] =res[0]['id']
            print(request.session['username'])
            return redirect(reverse('admin:index'))

    return render(request,'admin/login1.html')


def index(request):
    if 'uid' in request.session:
        username = request.session['username']
        print('&'*100)
        print(username)
        return render(request,'admin/index.html',context={'username':username})
    return render(request,'admin/index.html')


def productdetail(request):
    thrid = Category.objects.filter(classgrade=3).all()
    brands = Brand.objects.filter(brandstatus=0).all()
    warehouseinfo = Warehouseinfo.objects.filter(status=0).all()
    # print(thrid)
    if request.method=='POST':
        print('*'*80)
        goodsname = request.POST.get('goodsname')
        barcode = request.POST.get('barcode')
        brandid = request.POST.get('brand')
        brand = Brand.objects.get(pk=brandid)  #品牌名
        thridid = request.POST.get('category')   #三级分类的id
        print(thridid)
        threecategory = Category.objects.get(pk=thridid)  #根据id找到对应的对象
        secondid = threecategory.parentid   #拿到三级分类的父类id  就是二级分类id
        print(secondid)
        twocategory = Category.objects.get(pk = secondid)  #根据id找到对应的对象
        print(twocategory)
        firstid = twocategory.parentid  #拿到一级分类id
        warehouseid = request.POST.get('warehouse')  #仓库id
        nowcount = request.POST.get('nowcount')  #库存数量
        producttime = request.POST.get('producttime')
        validity = request.POST.get('validity')
        describe = request.POST.get('describe')
        Goods.objects.create(goodsname=goodsname,barcode=barcode,oneclassid=firstid,twoclassid=secondid,threeclassid=thridid,upstatus=0,producttime=producttime,validity=validity,describe=describe,brand=brand)
        goods = Goods.objects.last()
        goodsid = goods.id  #商品id
        # 商品库存表
        Repertory.objects.create(gid=goodsid, wid=warehouseid, nowcount=nowcount)

        file1 = request.FILES.get('photo1')
        file2 = request.FILES.get('photo2')
        file3 = request.FILES.get('photo3')
        path1 = os.path.join(settings.MEDIA_ROOT, file1.name)
        path2 = os.path.join(settings.MEDIA_ROOT, file2.name)
        path3 = os.path.join(settings.MEDIA_ROOT, file3.name)
        with open(path1, 'wb') as fp:
            # 如果文件超过2.5M,则分块读写
            if file1.multiple_chunks():
                for block1 in file1.chunks():
                    fp.write(block1)
            else:
                fp.write(file1.read())
        print(path1)
        with open(path2, 'wb') as fp:
            # 如果文件超过2.5M,则分块读写
            if file2.multiple_chunks():
                for block1 in file2.chunks():
                    fp.write(block1)
            else:
                fp.write(file2.read())
        print(path2)
        with open(path3, 'wb') as fp:
            # 如果文件超过2.5M,则分块读写
            if file3.multiple_chunks():
                for block1 in file3.chunks():
                    fp.write(block1)
            else:
                fp.write(file3.read())
        print(path3)
        path1 = '/' + path1
        path2 = '/' + path2
        path3 = '/' + path3
        Picture.objects.create(url=path1,main=0,order_by=1,valid=0,goods=goods)
        Picture.objects.create(url=path2,main=1,order_by=1,valid=0,goods=goods)
        Picture.objects.create(url=path3,main=1,order_by=1,valid=0,goods=goods)

        return render(request, 'admin/product_detail.html', context={
            'thrid': thrid, 'brands': brands,'warehouseinfo':warehouseinfo
        })
    return render(request, 'admin/product_detail.html', context={
        'thrid': thrid, 'brands': brands,'warehouseinfo':warehouseinfo
    })


def productlist(request):
    if request.method=='POST':
        categoryid = request.POST.get('category') #三级分类id
        print('$'*90)
        print(categoryid)
        goodslist = Goods.objects.filter(upstatus=0,threeclassid=categoryid).all()  # 商品查询结果集
    else:
        goodslist = Goods.objects.filter(upstatus=0).all()  # 商品查询结果集

    categorylist = Category.objects.filter(classgrade=3).all()
    repertorylist = Repertory.objects.all() #库存信息查询结果集
    snackslist = Snacks.objects.all()
    perfumelist = Perfume.objects.all()
    for goods in goodslist:
        picture = goods.picture_set.filter(main=0).first().url  #商品主图路径
        print(picture)
        goods.picture = picture
        for repertory in repertorylist:
            if goods.id == repertory.gid:
                goods.nowcount = repertory.nowcount
        for snacks in snackslist:
            if goods.id == snacks.goods.id:
                goods.price = snacks.price
        for perfume in perfumelist:
            if goods.id == perfume.goods.id:
                goods.price = perfume.price

    return render(request, 'admin/product_list.html',context={
        'categorylist':categorylist,'goodslist':goodslist,'repertorylist':repertorylist,'snackslist':snackslist,'perfumelist':perfumelist
    })

def userdetail(request,uid): #uid是用户的id
    user = User.objects.get(pk=uid)
    useraddr = user.useraddr_set.filter(isdefault=0).first()
    form = UserForm()
    if request.method=='POST':
        form = UserForm(request.POST)
        print(request.POST)
        if form.is_valid():
            print('-'*80)
            file = request.FILES.get('photo')
            print(file)
            print('+'*70)
            if file:
                path = os.path.join(settings.MEDIA_ROOT, file.name)
            # list = path.split('/')
            # print(path.split('/'))
            # path = '/'+ list[-3]+'/'+list[-2]+'/'+list[-1]
                print(path)
                print('+' * 70)
            # # 文件类型过滤
            # ext = os.path.splitext(file.name)
            # print(ext)
            # if len(ext) < 1 or not ext[1] in settings.ALLOWED_FILEEXTS:
            #     return redirect(reverse('admin:userdetail',kwargs={'uid':uid}))
                # 解决文件重名
            # if os.path.exists(path):
            #     # 日期目录
            #     dir = datetime.today().strftime("%Y/%m/%d")
            #     dir = os.path.join(settings.MEDIA_ROOT, dir)
            #     if not os.path.exists(dir):
            #         os.makedirs(dir)  # 递归创建目录
            #     # list.png
            #     file_name = ext[0] + datetime.today().strftime("%Y%m%d%H%M%S") + str(randint(1, 1000)) + ext[1] if len(ext) > 1 else ''
            #     path = os.path.join(dir, file_name)
            #     print(path)

                with open(path, 'wb') as fp:
                    # 如果文件超过2.5M,则分块读写
                    if file.multiple_chunks():
                        for block1 in file.chunks():
                            fp.write(block1)
                    else:
                        fp.write(file.read())
                print(path)
                user.picture = '/'+path


            user.username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            # user.password = hashlib.sha1(password.encode('utf8')).hexdigest()
            user.password=password
            user.ugrade = form.cleaned_data.get('ugrade')
            user.email = form.cleaned_data.get('email')
            user.phone = form.cleaned_data.get('phone')
            user.save()

            useraddr.province = form.cleaned_data.get('province')
            # print(useraddr.pro)
            useraddr.city = form.cleaned_data.get('city')
            useraddr.district = form.cleaned_data.get('district')
            useraddr.address = form.cleaned_data.get('address')
            useraddr.save()

            user = User.objects.get(pk=uid)
            useraddr = user.useraddr_set.filter(isdefault=0).first()
            return render(request, 'admin/user_detail.html', context={'user': user, 'useraddr': useraddr})
    return render(request,'admin/user_detail.html',context={'user':user,'useraddr':useraddr,'form':form})


def userlist(request):
    # userlist = User.objects.filter(usertype=0).all()
    # print('*'*100)
    # print(userlist)
    cursor = connection.cursor()
    cursor.execute("select * from user u join userlevel l on u.ugrade between l.mingrade and maxgrade where u.usertype=0")
    rows = cursor.fetchall()
    print(rows)
    return render(request,'admin/user_list.html',context={'rows':rows})


def userrank(request):
    return render(request,'admin/user_rank.html')


def rankstatistic(request):
    cursor = connection.cursor()
    cursor.execute("select l.levelname,count(*) from user u join userlevel l on u.ugrade between l.mingrade and maxgrade where u.usertype=0 group by l.levelname")
    rows = cursor.fetchall()
    print(rows)
    return render(request,'admin/discharge_statistic.html',context={
        'rows':rows
    })


def recyclebin(request):
    return render(request,'admin/recycle_bin.html')


def productdetailadd(request,gid,which=0):
    if request.method=='POST':
        print('*'*100)
        print(which)
        if which == '2':
            print('#'*100)

            goodsname = request.POST.get('goodsname')
            capacity = request.POST.get('capacity')
            color = request.POST.get('color')
            weight = request.POST.get('weight')
            place = request.POST.get('place')
            fragrance = request.POST.get('fragrance')
            addtime = request.POST.get('addtime')
            type = request.POST.get('type')
            character = request.POST.get('character')
            person = request.POST.get('person')
            pack = request.POST.get('pack')
            price = request.POST.get('price')
            goods = Goods.objects.get(pk=gid)  # 商品对象
            goods.goodsname = goodsname
            goods.save()  # 商品名更新
            Perfume.objects.create(capacity=capacity,color=color,weight=weight,place=place,fragrance=fragrance,addtime=addtime,type=type,character=character,person=person,pack=pack,price=price,goods=goods)
            perfume = Perfume.objects.last()
            return render(request, 'admin/product_detailadd.html', context={
                'goods': goods, 'which': 2,'perfume':perfume
            })
        else:
        # if which ==1:
            goodsname = request.POST.get('goodsname')
            specification = request.POST.get('specification')
            taste = request.POST.get('taste')
            weight = request.POST.get('weight')
            place = request.POST.get('place')
            safetime = request.POST.get('safetime')
            addtime = request.POST.get('addtime')
            allow_number =request.POST.get('allow_number')
            pack = request.POST.get('pack')
            price = request.POST.get('price')
            goods = Goods.objects.get(pk=gid)  #商品对象
            goods.goodsname = goodsname
            goods.save()        #商品名更新
            Snacks.objects.create(specification=specification,taste=taste,weight=weight,place=place,safetime=safetime,addtime=addtime,allow_number=allow_number,pack=pack,price=price,goods=goods)
            snacks = Snacks.objects.last()  #最新添加的snacks对象
            return render(request, 'admin/product_detailadd.html', context={
                'goods': goods, 'which': 1,'snacks':snacks
            })

    else:
        goods = Goods.objects.get(pk=gid)   #被编辑的商品对象
        # snackslist = Snacks.objects.all()
        # perfumelist = Perfume.objects.all()
        # for snacks in snackslist:
        if goods.threeclassid == 13:
            snacks = goods.snacks
            return render(request, 'admin/product_detailadd.html', context={
                'goods': goods,'which':1,'snacks':snacks
            })
        # for perfume in perfumelist:
        if goods.threeclassid == 12:
            perfume = goods.perfume
            return render(request,'admin/product_detailadd.html',context={
                'goods':goods,'which':2,'perfume':perfume
            })

#配送方式
def expresslist(request):
    return render(request,'admin/express_list.html')


def paylist(request):
    return render(request,'admin/pay_list.html')


def expressadd(request):
    return render(request,'admin/express_add.html')