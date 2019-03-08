"""
该文件中不能导入使用全局导入 app 中的 model, 因为 app docs 是第一被加载的且必须为第一加载项 :
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

import json
from functools import wraps
from django.views import View
from django.shortcuts import HttpResponse
from django.utils.six.moves.http_client import responses
from django.core.serializers.json import DjangoJSONEncoder


class Param(dict):
    """
    Parameters for building API documents.
    >>> Param('field_name', True, 'type', 'default_value', '备注')
    """

    def __init__(self, field_name, required, param_type, default='', description=''):
        """
        :param field_name: 字段名
        :param required: 是否必须
        :param param_type: 参数类型
        :param default: 默认值
        :param description: 描述
        """
        super(dict, self).__init__()
        self['field_name'] = field_name
        self['required'] = required
        self['param_type'] = param_type
        self['default'] = default
        self['description'] = description

    @property
    def kwargs(self):
        return {
            'field_name': self['field_name'],
            'required': self['required'],
            'param_type': self['param_type'],
            'default': self['default'],
            'description': self['description'],
        }


def api_define(name, url, params=[], desc='', headers=[]):
    if not headers:
        headers = [
            Param('authorization', False, 'str'),
        ]

    def foo(view):
        method = view.__name__
        router.register(view=view, name=name, url=url, params=params, method=method, desc=desc, headers=headers)

        @wraps(view)
        def inner(*args, **kwargs):
            return view(*args, **kwargs)

        return inner

    return foo


def login_required(method):
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        # TODO 登录校验
        return method(self, *args, **kwargs)

    return wrapper


class Response(HttpResponse):
    """
    An HTTP response class that consumes data to be serialized to JSON.

    :param data: Data to be dumped into json. By default only ``dict`` objects
      are allowed to be passed due to a security flaw before EcmaScript 5. See
      the ``safe`` parameter for more information.
    :param encoder: Should be an json encoder class. Defaults to
      ``django.core.serializers.json.DjangoJSONEncoder``.
    :param json_dumps_params: A dictionary of kwargs passed to json.dumps().
    """

    def __init__(self, data, status=None, content_type=None, encoder=DjangoJSONEncoder, json_dumps_params=None,
                 **kwargs):
        if json_dumps_params is None:
            json_dumps_params = {}
        # kwargs.setdefault('content_type', 'application/json')
        data = json.dumps(data, cls=encoder, **json_dumps_params)
        super(Response, self).__init__(content=data, content_type=content_type, status=status, **kwargs)

    @property
    def status_text(self):
        """
        Returns reason text corresponding to our HTTP response status code.
        Provided for convenience.
        """
        # TODO: Deprecate and use a template tag instead
        # TODO: Status code text for RFC 6585 status codes
        return responses.get(self.status_code, '')


class BaseHandler(View):
    @classmethod
    def as_view(cls, **initkwargs):
        """
        Set `cls' to use `allowed_methods' when building documents.
        """

        view = super(BaseHandler, cls).as_view(**initkwargs)
        view.cls = cls
        view.initkwargs = initkwargs
        return view

    @property
    def allowed_methods(self):
        """
        Wrap Django's private `_allowed_methods` interface in a public property.
        """
        return self._allowed_methods()

    def write(self, data, status=None, content_type=None, encoder=DjangoJSONEncoder, json_dumps_params=None, **kwargs):
        # status defaults to 200
        return Response(data=data, status=status, content_type=content_type)

    @property
    def ip(self):
        request = self.request
        if request.META.get('HTTP_X_FORWARDED_FOR'):
            ip = request.META['HTTP_X_FORWARDED_FOR']
        else:
            ip = request.META['REMOTE_ADDR']
        return ip
