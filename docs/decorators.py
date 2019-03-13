#!/usr/bin/env python
# -*- coding:utf-8 -*-
# __author__ = "lyon"

"""
docs 中不能导入使用全局导入 app 中的 model, 因为 app docs 会在其他 app 之前加载完成:
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
from django.conf import settings
from docs.routers import router
from docs.checks import params_check


def api_define(name, url, params=None, headers=None, desc='',
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

    # 如果apps中的ready没有加载, 则重新加载一次
    if not hasattr(settings, 'DEFAULT_PARAMS'):
        from docs import settings as docs_settings
        for i in dir(docs_settings):
            setting_value = getattr(docs_settings, i)
            setattr(settings, i, setting_value)

    params_list = list(settings.DEFAULT_PARAMS)
    if params is not None:
        params_list.extend(list(params))

    headers_list = list(settings.DEFAULT_HEADERS)
    if headers is not None:
        headers_list.extend(list(headers))

    def decorator(view):
        method = view.__name__
        router.register(view=view, name=name, url=url, params=params_check(params_list),
                        headers=params_check(headers_list),
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
