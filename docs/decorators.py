#!/usr/bin/env python
# -*- coding:utf-8 -*-
# __author__ = "lyon"

"""
docs 中不能导入使用全局导入 app 中的 model, 因为 app docs 是第一被加载的且必须为第一加载项 :
    1. model 与 App存在绑定关系, 必须 Install App 才能使用
    2. 为了使 api 能够自动进行注册路由, 在根目录的文件夹下的 urls.py 中进行自动加载
        - urls.py

            >>> from django.conf.urls import url, include
            >>> from django.contrib import admin
            >>> from docs import router
            >>> urlpatterns = [
            >>>    url(r'^docs/', include('docs.urls')),
            >>> ]
            >>> urlpatterns += router.urls

        - urls.py 为Django自动加载项
        - 通过settings中的 INSTALLED_HANDLERS 设置需要加载的 api
"""

from functools import wraps
from docs.routers import router
from docs.checks import params_check
from docs import settings as docs_settings


def api_define(name, url, params=docs_settings.DEFAULT_PARAMS, headers=docs_settings.DEFAULT_HEADERS, desc='',
               display=True):
    """
    :param name: api name 即 url() 中的name参数
    :param url: api url
    :param params: api 请求需要的参数
    :param headers: api 请求需要的请求头参数
    :param desc: api 描述
    :param display: 是否在文档上显示
    :return:
    """

    def decorator(view):
        method = view.__name__
        router.register(view=view, name=name, url=url, params=params_check(params), headers=params_check(headers),
                        desc=desc, method=method,
                        display=display)

        @wraps(view)
        def handler(*args, **kwargs):
            return view(*args, **kwargs)

        return handler

    return decorator


def login_required(method):
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        :param self: BaseHandler Object
        :param args:
        :param kwargs:
        :return:
        """
        # TODO 登录校验
        return method(self, *args, **kwargs)

    return wrapper
