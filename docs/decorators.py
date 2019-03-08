#!/usr/bin/env python
# -*- coding:utf-8 -*-
# __author__ = "lyon"

from functools import wraps
from docs.handler import Param
from docs.routers import router

def api_define(name, url, params=[], headers=[], desc='', display=True):
    """
    :param name: api name 即 url() 中的name参数
    :param url: api url
    :param params: api 请求需要的参数
    :param headers: api 请求需要的请求头参数
    :param desc: api 描述
    :param display: 是否在文档上显示
    :return:
    """
    if not headers:
        headers = [
            Param('authorization', False, 'str'),
        ]
    def api(view):
        method = view.__name__
        router.register(view=view, name=name, url=url, params=params, method=method, desc=desc, headers=headers, display=display)
        @wraps(view)
        def handler(*args, **kwargs):
            return view(*args, **kwargs)
        return handler
    return api


def login_required(method):
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        # TODO 登录校验
        return method(self, *args, **kwargs)
    return wrapper