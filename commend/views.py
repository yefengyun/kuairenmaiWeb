from django.shortcuts import render, redirect
from django.http import HttpResponse
from commend.models import *
from user.common import *
from user.views import checklogin, addusername
from django.db.models import Q
import datetime
import json
from django.core.paginator import Paginator


# Create your views here.
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
    permaxnum = 8  # 每页最多显示
    maxpage = 8  # 最大显示页码数量
    content = {}  # 传输字典
    try:
        page = strtoint(kwargs['page'])  # 页数
    except Exception:
        page = 1
    un = request.session.get('username')  # 获取当前用户帐号
    if un:
        content['username'] = un

    # 查询全部需求
    demandlist = Demand.objects.all().order_by('-starttime').values('id', 'title', 'starttime', 'money', 'count',
                                                                    'msglevel', 'uerid', 'catagoryid')
    p = Paginator(demandlist, permaxnum)  # 按每页最多permaxnum进行分页
    allpage = p.num_pages  # 总页数
    content['numpages'] = allpage

    pagerange = p.page_range  # 全部分页范围从1开始

    # 选取合适的maxpage页码
    if content['numpages'] > maxpage:
        if page < maxpage / 2:
            pagerange = pagerange[:maxpage]
        elif allpage - page > maxpage / 2:
            pagerange = pagerange[allpage - maxpage:]
        else:
            pagerange = pagerange[page - maxpage / 2:page + maxpage / 2]
    content['allpage'] = pagerange

    # 取对应页对象
    demands = p.page(page)
    content['pageobj'] = demands
    rslist = []  # 存储分装好的数据
    for demand in demands:  # 封装
        rsdir = {'demand': demand}
        user = usermodels.Userinfo.objects.get(pk=demand['uerid'])
        rsdir['user_headimg'] = user.headimg
        rsdir['user_nickname'] = user.nickname if user.nickname else user.username
        rsdir['user_vip'] = user.vip
        classob = Classification.objects.get(pk=demand['catagoryid'])
        rsdir['catagory'] = classob.catagory
        rslist.append(rsdir)
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
    content['demandlist'] = rslist
    return render(request, 'demand/search.html', content)


# 几天最热
def ndayhot(request):
    day = strtoint(request.GET.get('day'), 1)  # 获取前端传来天数

    content = {}
    yesteday = datetime.datetime.now() - datetime.timedelta(hours=23 * day, minutes=59, seconds=59)  # 前day天
    # 获取前一天的所有数据,按浏览次数排序
    dlist = Demand.objects.filter(starttime__gte=yesteday).order_by('-count').values('id', 'title', 'catagoryid')
    if len(dlist) > 8:  # 取钱面8条数据
        dlist = dlist[:8]
    rslist = []
    for d in dlist:
        cls = Classification.objects.get(pk=d['catagoryid'])
        d['cls'] = cls.catagory
        rslist.append(d)
        del d['catagoryid']
    content['rslist'] = rslist
    content = addusername(content, request)
    return HttpResponse(json.dumps(content), content_type="application/json")
