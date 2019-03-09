#!/usr/bin/env python
# -*- coding:utf-8 -*-
# __author__ = "lyon"

from functools import wraps
from docs.handler import Param
from docs.routers import router
from django.utils.translation import ugettext as _


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
    if not isinstance(params, list):
        raise TypeError(_('params type must be a list not %s.' % type(params)))
    if not isinstance(headers, list):
        raise TypeError(_('headers type must be a list not %s.' % type(headers)))
    for p in params:
        if not isinstance(p, Param):
            raise TypeError(_('api params %s should be a Param object not %s.' % (p, type(p).__name__)))
    for h in headers:
        if not isinstance(h, Param):
            raise TypeError(_('api headers %s should be a Param object not %s.' % (h, type(h).__name__)))

    if not headers:
        headers = [
            Param('authorization', False, 'str'),
        ]

    def decorator(view):
        method = view.__name__
        router.register(view=view, name=name, url=url, params=params, method=method, desc=desc, headers=headers,
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
