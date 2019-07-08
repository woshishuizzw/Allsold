from django.conf.urls import url

from App import views

urlpatterns = [
    url(r"^$", views.index, name="index"),
    url(r"^register/$", views.register, name="register"),
    url(r"^login/$", views.dologin, name="login"),
    url(r"^logout/$", views.dologout, name="logout"),
    url(r"^send/$", views.sendone, name="send"),
    url(r"^member/$", views.member, name="member"),
    url(r"^memberaddress/$", views.memberaddress, name="memberaddress"),
    url(r"^memberorder/$", views.memberorder, name="memberorder"),
    url(r"^membercollect/$", views.membercollect, name="membercollect"),
    url(r"^membersafe/$", views.membersafe, name="membersafe"),
    url(r"^getpassword/$", views.getpassword, name="getpassword"),

]