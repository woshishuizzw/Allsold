import hashlib

from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse

from App.models import *


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

