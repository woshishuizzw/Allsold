from django.conf.urls import url

from admin import views

urlpatterns = [
    url(r'^login/$',views.login,name='login'),
    url(r'^index/$',views.index,name='index'),
    url(r'^userdetail/$',views.userdetail,name='userdetail'),
    url(r'^userdetail/(?P<uid>\d+)/$',views.userdetail,name='userdetail'),
    url(r'^userlist/$',views.userlist,name='userlist'),
    url(r'^userrank/$',views.userrank,name='userrank'),
    url(r'^rankstatistic$',views.rankstatistic,name='rankstatistic'), #用户等级统计
    url(r'productlist',views.productlist,name='productlist'),
    url(r'productdetail',views.productdetail,name='productdetail'),
    url(r'recyclebin',views.recyclebin,name='recyclebin'),


]
