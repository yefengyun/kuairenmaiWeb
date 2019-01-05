# coding=utf-8
from django.http import HttpResponse


def router(request, **kwargs):
    """
    自动路由系统
    :param request: 请求
    :param kwargs: 字段
    :return:
    """
    appandfun = ['app', 'function']
    app = kwargs.get(appandfun[0], None)
    fun = kwargs.get(appandfun[1], None)

    newkwargs = {}
    for key, value in kwargs.items():
        if key not in appandfun:
            newkwargs[key] = value

    try:
        appObj = __import__("{}.views".format(app))
        viewObj = getattr(appObj, 'views')
        funObj = getattr(viewObj, fun)
        result = funObj(request, **newkwargs)

    except (ImportError, AttributeError) as e:
        print(e)
        return HttpResponse("404 Forbidden\n{}".format(e))
    except Exception as e:
        print(e)
        return HttpResponse("404 Error\n{}".format(e))
    return result
