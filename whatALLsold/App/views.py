import hashlib
from random import randint

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings

from App.models import User
from .forms import RegForm, LoginForm, GetpasswordForm


# Create your views here.
def index(request):
    return render(request, "app/Index.html")


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