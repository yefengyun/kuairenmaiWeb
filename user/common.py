from hashlib import md5
from PIL import Image, ImageDraw, ImageFont
import http.client
import urllib.request
import random


def cmd5(passwd):
    """
    使用md5加密
    :param passwd:密码
    :return: 加密后的密码
    """
    md = md5()
    md.update(passwd.encode('utf-8'))
    return md.hexdigest()


def rands(heigt):
    """
    获取随机整数
    :param heigt:0-heigt之间的整数
    :return: 随机整数
    """
    return random.randrange(heigt)


def genCode(width, height, fontsize=28):
    """
    生成随机验证码
    :param width:宽度
    :param height: 高度
    :param fontsize: 字体大小
    :return: 图相和验证码
    """
    size = (width, height)
    bgcolor = (rands(255), rands(255), 125)
    fbgcolor = (255 - bgcolor[0], 255 - bgcolor[1], 255 - bgcolor[2])
    im = Image.new("RGB", size, bgcolor)
    draw = ImageDraw.Draw(im)
    for i in range(50):
        xy = (rands(size[0]), rands(size[1]))
        cols = (rands(255), 255, rands(255))
        draw.point(xy, cols)

    for i in range(5):
        xy = (rands(size[0]), rands(size[0]), rands(size[1]), rands(size[1]))
        cols = (rands(255), 0, rands(255))
        draw.line(xy, cols, width=1)

    font = ImageFont.truetype("FreeMono.ttf", fontsize)
    rs = ""
    str = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for i in range(4):
        char = str[rands(len(str))]
        rs += char
        draw.text(((fontsize - 10) * i, random.randint(-5, 8)), char, fbgcolor, font)
    return im, rs


def send_message(phone):
    """
    发送短信验证码
    :param phone:电话号码
    :return:
    """
    # 请求的路径
    host = "106.ihuyi.com"
    sms_send_uri = "/webservice/sms.php?method=Submit"
    # 用户名是登录ihuyi.com账号名（例如：cf_demo123）
    account = "C60800740"
    # 密码 查看密码请登录用户中心->验证码、通知短信->帐户及签名设置->APIKEY
    password = "23f81d960b2eabce746381cdc7d23afe "

    # 定义一个字符串,存储生成的6位数验证码
    message_code = ''
    for i in range(6):
        i = random.randint(0, 9)
        message_code += str(i)
    # 拼接成发出的短信
    text = "您的验证码是：" + message_code + "。请不要把验证码泄露给其他人。"
    # 把请求参数编码
    params = urllib.parse.urlencode(
        {'account': account, 'password': password, 'content': text, 'mobile': phone, 'format': 'json'})
    # 请求头
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    # 通过全局的host去连接服务器
    conn = http.client.HTTPConnection(host, port=80, timeout=30)
    # 向连接后的服务器发送post请求,路径sms_send_uri是全局变量,参数,请求头
    conn.request("POST", sms_send_uri, params, headers)
    # 得到服务器的响应
    response = conn.getresponse()
    # 获取响应的数据
    response_str = response.read()
    # 关闭连接
    conn.close()
    return message_code, response_str


def strtoint(obj, default=1):
    """
    字符转数字
    :param obj:
    :param default:
    :return:
    """
    try:
        rs = int(obj)
    except Exception:
        rs = default
    return rs
