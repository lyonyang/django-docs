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
            >>> from django_docs import router
            >>> urlpatterns = [
            >>>    url(r'^docs/', include('django_docs.urls')),
            >>> ]
            >>> urlpatterns += router.urls

        - urls.py 为Django自动加载项
        - 通过settings中的 INSTALLED_HANDLERS 设置需要加载的 api
"""

from functools import wraps
from django.conf import settings
from .routers import router
from .checks import params_check, settings_check


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
    # 检查settings, 如果没有就设置
    settings_check()

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


def login_required(handler):
    @wraps(handler)
    def _wrapped_view(self, *args, **kwargs):
        """
        :param self: BaseHandler Object
        :param args:
        :param kwargs:
        :return:
        """
        # TODO 认证
        return handler(self, *args, **kwargs)

    return _wrapped_view


def permission_required(handler):
    @wraps(handler)
    def _wrapped_view(self, *args, **kwargs):
        """
        :param self: BaseHandler Object
        :param args:
        :param kwargs:
        :return:
        """
        # TODO 权限
        return handler(self, *args, **kwargs)

    return _wrapped_view


def throttle_required(handler):
    @wraps(handler)
    def _wrapped_view(self, *args, **kwargs):
        """
        :param self: BaseHandler Object
        :param args:
        :param kwargs:
        :return:
        """
        # TODO 限流
        return handler(self, *args, **kwargs)

    return _wrapped_view
