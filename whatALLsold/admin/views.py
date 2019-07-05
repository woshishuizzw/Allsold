import hashlib

import os
from datetime import datetime
from random import randint

from django.db import connection
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
            user.password = hashlib.sha1(password.encode('utf8')).hexdigest()
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


def productlist(request):
    return render(request,'admin/product_list.html')


def productdetail(request):
    thrid = Category.objects.filter(classgrade=3).all()
    brands = Brand.objects.filter(brandstatus=0).all()
    print(thrid)
    return render(request,'admin/product_detail.html',context={
        'thrid':thrid,'brands':brands
    })


def recyclebin(request):
    return render(request,'admin/recycle_bin.html')

