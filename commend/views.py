from django.shortcuts import render, redirect
from commend.models import *
from user.common import *
from django.db.models import Q


# Create your views here.
# 装饰器检查是否登录
def checklogin(myfunc):
    def check(request, *args, **kwargs):
        if request.session.get('username'):
            return myfunc(request, *args, **kwargs)
        else:
            return redirect("/user/login/")

    return check


# 字典添加username
def addusername(content, request):
    content['username'] = request.session.get('username')
    return content


# 需求发布页面
@checklogin
def demand(request):
    content = {}  # 传出字典
    un = request.session.get('username')  # 获取用户账户
    content['username'] = un  # 设置账户名
    cf = Classification.objects.all()  # 查询所有分类
    content['classobj'] = cf
    user = usermodels.Userinfo.objects.get(username=un)  # 查询指定用户
    content['nikename'] = user.nickname  # 用户别名
    content['wechar'] = user.wechar  # 用户威信
    content['phone'] = user.phone_number  # 用户电话
    content['qq'] = user.QQ  # 用户QQ
    return render(request, 'demand/demandnew.html', content)


# 需求发布页面-保存逻辑
@checklogin
def publishdemand(request):
    content = {}  # 传出字典
    if request.method == "POST":  # 只接受post请求
        title = request.POST.get("zname")  # 获取表单数据
        catagoryid = request.POST.get("industry")
        area = request.POST.get("diqu2")
        othername = request.POST.get("nickname")
        wechar = request.POST.get("wechat")
        tel = request.POST.get("zphone")
        QQ = request.POST.get("zqq")
        endtime = request.POST.get("jztime")
        comment = request.POST.get("tigongss")
        image = request.FILES.get('imgfile')
        money = request.POST.get("somoney")

        demand = Demand()  # 新建需求
        un = request.session.get('username')  # 获取用户帐号
        content['username'] = un
        user = usermodels.Userinfo.objects.get(username=un)  # 获取用户
        demand.uerid = user  # 设置需求
        demand.title = title
        cl = Classification.objects.get(id=catagoryid)
        demand.catagoryid = cl
        demand.area = area
        demand.othername = othername
        demand.wechar = wechar
        demand.tel = tel
        demand.QQ = QQ
        demand.endtime = endtime
        demand.comment = comment
        demand.image = image
        demand.money = money
        demand.save()
        return render(request, 'index.html', content)
    else:
        return redirect("/user/login/")


# 首页
def index(request, **kwargs):
    content = {}  # 传输字典
    try:
        page = strtoint(kwargs['page'])  # 页数
    except Exception:
        page = 1
    content['page'] = page
    un = request.session.get('username')  # 获取当前用户帐号
    if un:
        content['username'] = un

    # 查询全部需求
    demandlist = Demand.objects.all().order_by('starttime').values('id', 'title', 'starttime', 'money', 'count',
                                                                   'msglevel', 'uerid', 'catagoryid')
    rslist = []
    for demand in demandlist:  # 封装
        rsdir = {'demand': demand}
        user = usermodels.Userinfo.objects.get(pk=demand['uerid'])
        rsdir['user_headimg'] = user.headimg
        rsdir['user_nickname'] = user.nickname if user.nickname else user.username
        rsdir['user_vip'] = user.vip
        classob = Classification.objects.get(pk=demand['catagoryid'])
        rsdir['catagory'] = classob.catagory
        rslist.append(rsdir)
        print(user.vip)
    content['demandlist'] = rslist
    return render(request, 'index.html', content)


# 搜索
def search(request, **kwargs):
    content = {}  # 传输字典
    try:
        page = strtoint(kwargs['page'])  # 页数
    except Exception:
        page = 1
    content['page'] = page
    un = request.session.get('username')  # 获取当前用户帐号
    if un:
        content['username'] = un

    context = request.GET.get('so')
    if context:
        # 查询全部需求
        demandlist = Demand.objects.filter(
            Q(title__contains=context) | Q(comment__contains=context) | Q(othername__contains=context)).order_by(
            'starttime').values('id', 'title', 'starttime', 'money', 'count', 'msglevel', 'uerid', 'catagoryid')
    else:
        # 查询全部需求
        demandlist = Demand.objects.filter().order_by('starttime').values('id', 'title', 'starttime', 'money', 'count',
                                                                       'msglevel', 'uerid', 'catagoryid')
    rslist = []
    for demand in demandlist:  # 封装
        rsdir = {'demand': demand}
        user = usermodels.Userinfo.objects.get(pk=demand['uerid'])
        rsdir['user_headimg'] = user.headimg
        rsdir['user_nickname'] = user.nickname if user.nickname else user.username
        rsdir['user_vip'] = user.vip
        classob = Classification.objects.get(pk=demand['catagoryid'])
        rsdir['catagory'] = classob.catagory
        rslist.append(rsdir)
        print(user.vip)
    content['demandlist'] = rslist
    return render(request, 'demand/search.html', content)
