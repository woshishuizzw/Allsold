from datetime import datetime

from django.db import models


# Create your models here.


class User(models.Model):
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=200)
    email = models.CharField(max_length=25)
    phone = models.CharField(max_length=11, null=True)
    sex = models.BooleanField(default=True) # 1表示女0表示男
    ugrade = models.IntegerField(default=0) # 用户积分
    # regtime = models.CharField(max_length=100, null=True)
    brithday = models.CharField(max_length=12, null=True)
    balance = models.FloatField(default=0) # 用户余额
    usertype = models.BooleanField(default=False)# 0 普通 1 管理员
    papers = models.CharField(max_length=5, default="身份证") # 证件类型
    papersid = models.CharField(max_length=23) # 证件id
    picture = models.CharField(max_length=300, default="/static/app/images/default.jpg")


    class Meta:
        db_table = "user"



# 级别表
class Userlevel(models.Model):
    levelname = models.CharField(max_length=10)
    mingrade = models.IntegerField() # 最低分
    maxgrade = models.IntegerField() # 最高分

    class Meta:
        db_table = "userlevel"



# 用户地址表
class Useraddr(models.Model):
    province = models.CharField(max_length=30, null=True)
    city = models.CharField(max_length=30, null=True)
    district = models.CharField(max_length=30, null=True)
    address = models.CharField(max_length=100, null=True) # 详细地址
    isdefault = models.BooleanField(default=False) # 是否默认 0默认1不默认
    changetime = models.DateTimeField(auto_now=True)  #修改时间
    consignee = models.CharField(max_length=5, null=True) # 收货人
    phone = models.CharField(max_length=11, null=True) # 手机
    tel = models.CharField(max_length=15, null=True) # 电话
    email = models.CharField(max_length=20, null=True)
    postcode = models.IntegerField(null=True) # 邮编
    user = models.ForeignKey(to="User", on_delete=models.CASCADE, db_column="uid")

    class Meta:
        db_table = "useraddr"


# 积分变更日志表
class Gradelog(models.Model):
    source = models.BooleanField(default=False) # 积分来源 0订单 1活动
    correlationid = models.IntegerField() # 积分来源相关编号
    num = models.IntegerField(default=5) # 变更分数
    changetime = models.DateTimeField(auto_now_add=True) # 变更时间
    user = models.ForeignKey(to="User", on_delete=models.CASCADE, db_column="uid")
    
    class Meta:
        db_table = "gradelog"


# 余额变更日志
class Balancelog(models.Model):
    source = models.IntegerField(default=1) # 变更来源 1 订单 2 退货 3 红包
    correlationid = models.IntegerField() # 变更来源相关id
    money = models.FloatField() # 变更钱数
    changetime = models.DateTimeField(auto_now_add=True) # 变更时间
    user = models.ForeignKey(to="User", on_delete=models.CASCADE, db_column="uid")

    class Meta:
        db_table = "balancelog"



# 登录日志
class Loginlog(models.Model):
    logintime = models.DateTimeField(auto_now_add=True)
    loginip = models.CharField(max_length=15)
    logintype = models.BooleanField(default=False) # 0表示成功 1未成功
    user = models.ForeignKey(to="User", on_delete=models.CASCADE, db_column="uid")

    class Meta:
        db_table = "loginlog"


# 品牌信息表
class Brand(models.Model):
    brandname = models.CharField(max_length=30)
    logourl = models.CharField(max_length=100, null=True) # logo路径
    describe = models.CharField(max_length=200, null=True) # 品牌描述
    brandstatus = models.BooleanField(default=False) #品牌状态 0启用 1禁用
    orderby = models.IntegerField()   # 排序
    category = models.ForeignKey(to="Category", on_delete=models.CASCADE, db_column="cid", null=True) # 所属板块

    class Meta:
        db_table = "brand"


# 分类信息表
class Category(models.Model):
    classname = models.CharField(max_length=30)
    parentid = models.IntegerField(default=0) # 父类id
    classgrade = models.IntegerField() # 分类级别

    class Meta:
        db_table = "category"


# 商品信息表
class Goods(models.Model):
    goodsname = models.CharField(max_length=30)
    barcode = models.CharField(max_length=50) # 条形码
    oneclassid = models.IntegerField() # 一级分类id
    twoclassid = models.IntegerField() # 二级分类id
    threeclassid = models.IntegerField() # 三级分类id
    upstatus = models.BooleanField(default=False) # 上架状态 0上架 1下架
    producttime = models.CharField(max_length=30) # 生产日期
    validity = models.CharField(max_length=5) # 有效期
    describe = models.CharField(max_length=200, null=True) # 商品描述
    brand = models.ForeignKey(to="Brand", on_delete=models.CASCADE, db_column="bid")# 品牌id
    lookcount = models.IntegerField(default=0) # 浏览次数

    class Meta:
        db_table = "goods"


# 物流公司信息表
class Logistics(models.Model):
    lname = models.CharField(max_length=30, unique=True)  # 物流公司名称
    linkman = models.CharField(max_length=30)  # 物流公司联系人
    telephone = models.CharField(max_length=30, unique=True)  # 联系电话
    price = models.FloatField()  # 配送价格

    class Meta:
        db_table = 'logistics'  # 物流


# 商品库存表
class Repertory(models.Model):
    gid = models.IntegerField(unique=True)  # 商品id
    wid = models.IntegerField()  # 仓库id
    nowcount = models.IntegerField()  # 当前商品数量

    class Meta:
        db_table = 'repertory'  # 库存


# 仓库信息表
class Warehouseinfo(models.Model):
    warename = models.CharField(max_length=30, unique=True)  # 仓库名称
    linkman = models.CharField(max_length=30)  # 仓库联系人
    telephone = models.CharField(max_length=30, unique=True)  # 仓库电话
    province = models.CharField(max_length=10)  # 省
    city = models.CharField(max_length=10)  # 市
    area = models.CharField(max_length=10)  # 区
    address = models.CharField(max_length=50)  # 仓库详细地址
    status = models.IntegerField(default=0)  # 仓库状态 0启用 1禁用  默认0

    class Meta:
        db_table = 'warehouseinfo'  # 仓库信息


# 购物车表
class Shoppingcart(models.Model):
    user = models.ForeignKey(to="User", on_delete=models.CASCADE, db_column="uid", null=True)    # 用户id
    goods = models.ForeignKey(to="Goods", on_delete=models.CASCADE, db_column="gid", null=True)  # 商品id
    count = models.IntegerField(default=0)  # 加入购物车商品数量  默认误0
    price = models.FloatField()  # 商品价格
    addtime = models.DateTimeField(auto_now_add=True)  # 加入购物车时间

    class Meta:
        db_table = 'shoppingcart'


# 订单表
class Order(models.Model):
    onumber = models.CharField(max_length=30, unique=True)  # 订单编号
    user = models.ForeignKey(to="User", on_delete=models.CASCADE, db_column="uid")# 下单人id  就是用户id
    getername = models.CharField(max_length=30)  # 收货人姓名
    province = models.CharField(max_length=10)  # 省
    city = models.CharField(max_length=10)  # 市
    area = models.CharField(max_length=10)  # 区
    address = models.CharField(max_length=50)  # 详细地址
    phone = models.CharField(max_length=11, null=True) # 收货人电话
    paymothod = models.IntegerField(default=1)  # 支付方式  1--余额  2--网银 2--支付宝  4--微信
    money = models.FloatField()  # 订单金额
    lname = models.CharField(max_length=30, default="申通快递")  # 物流公司名称
    lnumber = models.CharField(max_length=30, unique=True)  # 快递单号
    ordertime = models.DateTimeField(auto_now_add=True)  # 下单时间
    delivertime = models.DateTimeField(null=True)  # 发货时间
    paytime = models.DateTimeField(null=True)  # 支付时间
    orderstatus = models.IntegerField(default=2)  # 1--待付款  2--待收货  3--已完成  4--已取消 5-待评论
    grade = models.IntegerField(default=5)  # 订单积分  默认一单五分
    count = models.IntegerField(default=1)  # 购买商品数量
    unitprice = models.FloatField(null=True)  # 购买商品单价
    weight = models.FloatField(default=0)  # 商品重量
    wid = models.IntegerField(default=1)  # 仓库id
    goods = models.ForeignKey(to="Goods", db_column="gid",on_delete=models.CASCADE, null=True)  # 订单商品id
    class Meta:
        db_table = 'order'


# 商品评论表
class Comment(models.Model):
    goods = models.ForeignKey(to="Goods", on_delete=models.CASCADE, db_column="gid") # 商品id
    oid = models.IntegerField()  # 订单id
    user = models.ForeignKey(to="User", on_delete=models.CASCADE, db_column="uid")# 用户id
    title = models.CharField(max_length=20)  # 评论标题
    content = models.CharField(max_length=300)  # 评论内容
    time = models.DateTimeField(auto_now_add=True)  # 评论时间

    class Meta:
        db_table = 'comment'


# 商品图片表
class Picture(models.Model):
    url = models.CharField(max_length=200)
    main = models.IntegerField()  # 是否主图  0主  1不是
    order_by = models.IntegerField()  # 图片排序
    valid = models.IntegerField()  # 图片是否有效  0有效 1无效
    goods = models.ForeignKey(to="Goods", on_delete=models.CASCADE, db_column="gid")

    class Meta:
        db_table = 'picture'


# 零食属性表
class Snacks(models.Model):
    specification = models.CharField(max_length=30)  # 规格
    taste = models.CharField(max_length=30)  # 口味
    weight = models.FloatField()  # 毛重
    place = models.CharField(max_length=30)  # 产地
    addtime = models.DateTimeField(auto_now_add=True)  # 商品上架时间
    safetime = models.CharField(max_length=30)  # 保质期
    allow_number = models.IntegerField()  # 生产许可证号
    pack = models.CharField(max_length=20)  # 商品包装
    price = models.FloatField()  # 价格
    goods = models.OneToOneField(to="Goods", on_delete=models.CASCADE, db_column="gid", null=True)

    class Meta:
        db_table = 'snacks'


# 香水属性表
class Perfume(models.Model):
    capacity = models.CharField(max_length=10)  # 容量
    color = models.CharField(max_length=10)  # 颜色
    weight = models.FloatField()  # 毛重
    place = models.CharField(max_length=30)  # 产地
    fragrance = models.CharField(max_length=30)  # 香调
    addtime = models.DateTimeField(auto_now_add=True)  # 商品上架时间
    type = models.CharField(max_length=30)  # 类型
    character = models.CharField(max_length=30)  # 商品质地
    person = models.CharField(max_length=30)  # 适合人群
    pack = models.CharField(max_length=20)  # 商品包装
    price = models.FloatField()  # 价格
    goods = models.OneToOneField(to="Goods", on_delete=models.CASCADE, db_column="gid", null=True)

    class Meta:
        db_table = 'perfume'

# 收藏表
class Collect(models.Model):
    goods = models.ForeignKey(to="Goods", on_delete=models.CASCADE, db_column="gid")
    user = models.ForeignKey(to="User", on_delete=models.CASCADE, db_column="uid")
    collecttime = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "collect"

# 浏览记录表
class Lookhistory(models.Model):
    user = models.ForeignKey(to="User", on_delete=models.CASCADE, db_column="uid")
    goods = models.ForeignKey(to="Goods", on_delete=models.CASCADE, db_column="gid")
    looktime = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        db_table = "lookhistory"


class Flow(models.Model):
    ftime = models.CharField(max_length=20)
    view = models.IntegerField()

    class Meta:
        db_table = "flow"