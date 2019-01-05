from django.db import models


# Create your models here.
# 用户类
class Userinfo(models.Model):
    username = models.CharField(max_length=20, null=False)  # 帐号
    password = models.CharField(max_length=64, null=False)  # 密码
    nickname = models.CharField(max_length=20, null=True, default="")  # 昵称
    phone_number = models.CharField(max_length=11, null=False)  # 电话号码
    vip = models.IntegerField(default=0)  # 权限
    wechar = models.CharField(max_length=20, null=True, default="")  # 威信
    QQ = models.CharField(max_length=20, null=True, default="")  # qq
    email = models.EmailField(null=True, default="")  # 邮箱
    bankcard = models.CharField(max_length=20, null=True, default="")  # 银行卡
    headimg = models.ImageField(upload_to='user/', default='user/tx00.png')  # 头像
    requirement_count = models.IntegerField(default=0)  # 需求总数
    createtime = models.DateTimeField(auto_now=True)  # 创建时间

    class Meta:
        db_table = 'userinfo'  # 表名


# 行业类
class Job(models.Model):
    job = models.CharField(max_length=20)  # 行业

    class Meta:
        db_table = 'job'


# 职业类
class Professional(models.Model):
    userid = models.OneToOneField(Userinfo, on_delete=models.CASCADE)  # userid外鍵，关联Userinfo表的ID
    prosfession = models.CharField(max_length=50, null=False)  # 用户职业信息
    company = models.CharField(max_length=50, null=False)  # 用户的公司
    brand = models.CharField(max_length=20, null=False)  # 品牌
    office = models.CharField(max_length=20, null=False)  # 职位
    truename = models.CharField(max_length=20, null=True)  # 真实姓名
    companyintroducion = models.TextField(null=True)  # 公司简介
    jobs = models.ForeignKey(Job, on_delete=models.CASCADE, default=1)  # 所处行业

    class Meta:
        db_table = 'professional'  # 表明
