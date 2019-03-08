#!/usr/bin/env python
# -*- coding:utf-8 -*-
# __author__ = "lyon"

from functools import wraps
from docs.handler import Param
from docs.routers import router

def api_define(name, url, params=[], headers=[], desc=''):
    """
    :param name:
    :param url:
    :param params:
    :param desc:
    :param headers:
    :return:
    """
    if not headers:
        headers = [
            Param('authorization', False, 'str'),
        ]
    def api(view):
        method = view.__name__
        router.register(view=view, name=name, url=url, params=params, method=method, desc=desc, headers=headers)
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