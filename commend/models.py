from django.db import models
from user import models as usermodels


# Create your models here.
# 需求分类
class Classification(models.Model):
    catagory = models.CharField(max_length=20)

    class Meta:
        db_table = "classification"


# 需求表发布
class Demand(models.Model):
    # 信息发布者id，外键
    uerid = models.ForeignKey(usermodels.Userinfo, on_delete=models.CASCADE)
    # 发布标题
    title = models.CharField(max_length=50, null=False)
    # 发布内容
    comment = models.CharField(max_length=250, null=False)
    # 地域要求
    area = models.CharField(max_length=50)
    #称呼
    othername=models.CharField(max_length=20,default='')
    # 上传的图片
    image = models.ImageField(upload_to='demand/', default='demand/init.png')
    # 创建日期
    starttime = models.DateTimeField(auto_now=True)
    # 截止日期
    endtime = models.DateField(auto_now=False)
    # 赏金
    money = models.DecimalField(max_digits=10, decimal_places=2)
    # 联系方式
    wechar = models.CharField(max_length=20, null=False,default='')  # 威信
    QQ = models.CharField(max_length=20, null=True,default='')  # qq
    tel = models.CharField(max_length=11, null=True,default='')  # tel
    # 浏览次数
    count = models.IntegerField(default=0)
    # 需求分类
    catagoryid = models.ForeignKey(Classification, on_delete=models.CASCADE, default=1)
    # 是否解决
    iscomplete = models.BooleanField(default=False)
    # 是否置顶
    msglevel = models.BooleanField(default=False)

    class Meta:
        db_table = "demand"


