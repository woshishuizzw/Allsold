from django.conf.urls import url

from admin import views

urlpatterns = [
    url(r'^login/$',views.login,name='login'),
    url(r'^getcode/$',views.getcode,name='getcode'),
    url(r'^index/$',views.index,name='index'),
    url(r'^userdetail/$',views.userdetail,name='userdetail'),
    url(r'^userdetail/(?P<uid>\d+)/$',views.userdetail,name='userdetail'),
    url(r'^userlist/$',views.userlist,name='userlist'),
    url(r'^userlist/(\d+)/$',views.userlist,name='userlist'),
    url(r'^userrank/$',views.userrank,name='userrank'),
    url(r'^rankstatistic$',views.rankstatistic,name='rankstatistic'), #用户等级统计
    url(r'^productlist$',views.productlist,name='productlist'),
    url(r'^productdetail$',views.productdetail,name='productdetail'),
    url(r'^recyclebin$',views.recyclebin,name='recyclebin'),
    url(r'^recyclebin/(?P<gid>\d+)$',views.recyclebin,name='recyclebin'),
    url(r'^detelegoods/(?P<gid>\d+)$',views.detelegoods,name='detelegoods'),
    url(r'^restore/(?P<gid>\d+)$',views.restore,name='restore'),

    url(r'^productdetailadd/(?P<gid>\d+)/$',views.productdetailadd,name='productdetailadd'),
    url(r'^productdetailadd/(?P<gid>\d+)/(?P<which>\d+)$',views.productdetailadd,name='productdetailadd'),
    url(r'^expresslist$',views.expresslist,name='expresslist'),
    url(r'^paylist$',views.paylist,name='paylist'),
    url(r'^expressadd$',views.expressadd,name='expressadd'),
    url(r'^salesvolume$',views.salesvolume,name='salesvolume'),
    url(r'^orderlist$',views.orderlist,name='orderlist'),
    url(r'^flowstatictics$',views.flowstatistics,name='flowstatistics')
]
