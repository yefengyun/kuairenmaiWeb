from django.shortcuts import render, redirect
from django.http import HttpResponse
from user.models import *
from user import common
from io import BytesIO
import json


# Create your views here.
# 装饰器检查是否登录
def checklogin(myfunc):
    def check(request, *args, **kwargs):
        if request.session.get('username'):
            return myfunc(request, *args, **kwargs)
        else:
            return redirect("/user/login/")

    return check


# 主页
def index(request):
    # 获取用户账户
    username = request.session.get('username') if request.session.get('username') else None
    return render(request, 'index.html', {'username': username})


# 登录
def login(request):
    return render(request, 'login.html')


# 注销
@checklogin
def dellogin(request):
    del request.session['username']
    return redirect('/user/login/')


# 登录逻辑处理
def login_handler(request):
    # 信息
    resp = {'status': 400, 'data': '登录失败'}
    if request.method == "POST":  # 登录方式
        usernm = request.POST.get("username")  # 获取用户名
        passwd = request.POST.get("password")  # 获取密码

        user = Userinfo.objects.filter(username=usernm)  # 到数据库查询
        if len(user) == 1:
            print(common.cmd5(str(passwd)) == user[0].password)
            if common.cmd5(str(passwd)) == user[0].password:
                request.session['username'] = usernm
                resp['status'] = 200
                resp['data'] = 'success'
            else:
                resp['data'] = '密码错误'
        else:
            resp['data'] = '用户不存在'
        return HttpResponse(json.dumps(resp), content_type="application/json")
    else:
        return HttpResponse(json.dumps(resp), content_type="application/json")


# 注册
def register(request):
    return render(request, 'register.html')


# 注册处理逻辑
def register_handler(request):
    resp = {'status': 400, 'msg': '非法注册'}
    if request.method == "POST":
        # 获取字段
        username = request.POST.get('zphone')
        msgcode = request.POST.get('zcode1')
        passwd1 = request.POST.get('zpass')
        passwd2 = request.POST.get('zpass2')
        if (passwd1 == passwd2):
            if (request.session.get('msgcode') == msgcode):  # 验证码
                user = Userinfo()
                user.username = username
                print(passwd1)
                user.password = common.cmd5(str(passwd1))
                print(user.password)
                user.save()
                resp['status'] = 200
                resp['msg'] = '注册成功，请登录'
                return render(request, 'login.html', resp)
            else:
                resp['msg'] = '验证码不正确'
                return render(request, 'register.html', resp)
        else:
            resp['msg'] = '两次密码不一致'
            return render(request, 'register.html', resp)

    return render(request, 'register.html', resp)


# 发送短信验证码
def register_sendmessage(request):
    # 获取电话号码
    moblie = request.GET.get('phone')
    # print(moblie)
    # 通过手机去查找用户是否已经注册
    user = Userinfo.objects.filter(username=moblie)
    if len(user) == 1:
        resp = {'status': 400, 'msg': '该手机已注册'}
        return HttpResponse(json.dumps(resp), content_type="application/json")
    else:
        # msgcode, response_str = common.send_message(moblie)
        # print(msgcode, response_str)
        msgcode, response_str = '123456', b'{"code":2,"msg":"\\u63d0\\u4ea4\\u6210\\u529f","smsid":"15464153595432868415"}'
        request.session['msgcode'] = msgcode
        resp = {'status': 200, 'msg': response_str.decode()}
        return HttpResponse(json.dumps(resp), content_type="application/json")


# 发送短信验证码
def upass_sendmessage(request):
    # 获取电话号码
    moblie = request.GET.get('phone')
    # print(moblie)
    # 通过手机去查找用户是否已经注册
    user = Userinfo.objects.filter(username=moblie)
    if len(user) == 1:
        # msgcode, response_str = common.send_message(moblie)
        # print(msgcode, response_str)
        msgcode, response_str = '123456', b'{"code":2,"msg":"\\u63d0\\u4ea4\\u6210\\u529f","smsid":"15464153595432868415"}'
        request.session['msgcode'] = msgcode
        resp = {'status': 200, 'msg': response_str.decode()}
        return HttpResponse(json.dumps(resp), content_type="application/json")
    else:
        resp = {'status': 400, 'msg': '帐号不存在'}
        return HttpResponse(json.dumps(resp), content_type="application/json")


# 获取图像验证码
def getcodeimg(request):
    f = BytesIO()  # 返回字节流
    im, code = common.genCode(80, 40, 30)  # 获取验证码
    request.session['code'] = code.lower()  # 设置session验证码
    im.save(f, 'PNG')  # 将图像转为字节流

    return HttpResponse(f.getvalue(), "image/PNG")


# 获取验证码
def getcode(request):
    resp = {}
    resp['code'] = request.session.get('code')
    return HttpResponse(json.dumps(resp), content_type="application/json")


# 忘记密码
def upass(request):
    return render(request, 'upass.html')


# 忘记密码逻辑处理
def upass_handler(request):
    resp = {'status': 400, 'msg': '非法修改'}
    if request.method == "POST":
        # 获取字段
        username = request.POST.get('zphone')
        msgcode = request.POST.get('zcode1')
        passwd1 = request.POST.get('zpass')
        passwd2 = request.POST.get('zpass2')
        if (passwd1 == passwd2):
            if (request.session.get('msgcode') == msgcode):  # 验证码
                user = Userinfo.objects.filter(username=username)
                if len(user) == 1:
                    user = user[0]
                    user.password = common.cmd5(str(passwd1))
                    user.save()
                    resp['status'] = 200
                    resp['msg'] = '修改成功，请登录'
                    return render(request, 'login.html', resp)
                else:
                    resp['msg'] = '用户不存在'
                    return render(request, 'upass.html', resp)
            else:
                resp['msg'] = '验证码不正确'
                return render(request, 'upass.html', resp)
        else:
            resp['msg'] = '两次密码不一致'
            return render(request, 'upass.html', resp)

    return render(request, 'upass.html', resp)


# 字典添加username
def addusername(content, request):
    content['username'] = request.session.get('username')
    return content


# 个人中心-我的资料
@checklogin
def userindex(request):
    username = request.session.get('username')  # 获取登录用户名
    u = Userinfo.objects.filter(username=username)  # 获取用户对象
    if len(u) == 1:
        u = u[0]
        nkname = u.nickname  # 提取有用数据
        phone = u.phone_number if u.phone_number else u.username
        headimg = u.headimg
        vip = u.vip
        company = u.professional.company
        brand = u.professional.brand
        job = u.professional.office
        content = {'flag': 1, 'nkname': nkname, 'phone': phone, 'headimg': headimg, 'vip': vip,
                   'company': company, 'brand': brand, 'job': job}
        # print(content)
        return render(request, 'user/user.html', addusername(content, request))
    else:
        return redirect("/user/login/")


# 个人中心-我的特权
@checklogin
def uservip(request):
    username = request.session.get('username')  # 获取登录用户名
    u = Userinfo.objects.filter(username=username)  # 获取用户对象
    if len(u) == 1:
        u = u[0]
        vip = u.vip
        content = {'flag': 2, 'vip': vip}
        return render(request, 'user/vip.html', addusername(content, request))
    else:
        return redirect("/user/login")


# 个人中心-我的道具
@checklogin
def mytools(request):
    content = {'flag': 3}
    return render(request, 'user/mytools.html', addusername(content, request))


# 个人中心-我的消息
@checklogin
def mymessage(request):
    content = {'flag': 4}
    return render(request, 'user/message.html', addusername(content, request))


# 个人中心-职业信息
@checklogin
def account(request):
    content = {'flag': 1}
    jobs = Job.objects.all()
    content['jobs'] = jobs
    un = request.session.get('username')
    content['username'] = un
    user = Userinfo.objects.filter(username=un)
    if len(user) == 1:
        user = user[0]
        company = user.professional.company
        brand = user.professional.brand
        job = user.professional.office
        truename = user.professional.truename
        cpintroducion = user.professional.companyintroducion
        defjobid = user.professional.jobs.id
        content['company'] = company
        content['brand'] = brand
        content['job'] = job
        content['truename'] = truename
        content['cpintroducion'] = cpintroducion
        content['defjobid'] = defjobid
        # print(content)
        return render(request, 'user/accountinfo.html', content)

    return redirect("/user/login")


# 个人中心-职业信息-保存逻辑
@checklogin
def jobinfo(request):
    if request.method == 'POST':
        jobid = request.POST.get('industry')
        company = request.POST.get('company')
        brand = request.POST.get('brand')
        zjob = request.POST.get('zjob')
        xname = request.POST.get('xname')
        intro = request.POST.get('intro')
        un = request.session.get('username')
        user = Userinfo.objects.get(username=un)
        jobobj = Job.objects.get(pk=jobid)
        prof = Professional.objects.get(userid_id=user.id)
        prof.company = company
        prof.brand = brand
        prof.office = zjob
        prof.truename = xname
        prof.companyintroducion = intro
        prof.jobs = jobobj
        prof.save()
        content = {'flag': 1, 'msg': '修改成功'}
        content['company'] = company
        content['brand'] = brand
        content['job'] = zjob
        content['truename'] = xname
        jobs = Job.objects.all()
        content['jobs'] = jobs
        content['cpintroducion'] = intro
        content['defjobid'] = jobid
        return render(request, 'user/accountinfo.html', addusername(content, request))
    else:
        return redirect("/user/login/")


# 个人中心-联系方式
@checklogin
def contactway(request):
    content = {'flag': 2}
    un = request.session.get('username')
    user = Userinfo.objects.get(username=un)
    wechar = user.wechar
    qq = user.QQ
    email = user.email
    content['wechar'] = wechar
    content['qq'] = qq
    content['email'] = email
    return render(request, 'user/usercontactway.html', content)


# 个人中心-联系方式-保存逻辑
@checklogin
def contactwaysave(request):
    if request.method == 'POST':
        wechar = request.POST.get('wei')
        qq = request.POST.get('qq')
        email = request.POST.get('email')
        un = request.session.get('username')
        content = {'flag': 2, 'username': un}
        user = Userinfo.objects.get(username=un)
        user.wechar = wechar
        user.qq = qq
        user.email = email
        user.save()
        content['wechar'] = wechar
        content['qq'] = qq
        content['email'] = email
        content['msg'] = '修改成功'
        return render(request, 'user/usercontactway.html', content)
    else:
        return redirect("/user/login/")


# 个人中心-修改密码
@checklogin
def changepasswd(request):
    content = {'flag': 3}
    return render(request, 'user/changepasswd.html', addusername(content, request))


# 个人中心-修改密码-保存逻辑
@checklogin
def changepasswdsave(request):
    if request.method == 'POST':
        zpass = request.POST.get('zpass')
        npass = request.POST.get('npass')
        npass2 = request.POST.get('npass2')
        un = request.session.get('username')
        content = {'flag': 3, 'username': un}
        user = Userinfo.objects.get(username=un)

        if npass == npass2:
            if user.password == common.cmd5(zpass):
                user.password = common.cmd5(npass)
                user.save()
                content['msg'] = '密码修改成功'
            else:
                content['msg'] = '当前密码正确'
        else:
            content['msg'] = '两次密码不一致'
        return render(request, 'user/changepasswd.html', content)
    else:
        return redirect("/user/login/")
