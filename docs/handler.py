#!/usr/bin/env python
# -*- coding:utf-8 -*-
# __author__ = "lyon"

from __future__ import unicode_literals

import json
from django.views import View
from django.shortcuts import HttpResponse
from django.utils.encoding import force_str
from django.core.serializers.json import DjangoJSONEncoder


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


class BaseHandler(View):
    """
    Handler for handling HTTP requests.
    """

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

    @classmethod
    def force_http_method_names(cls):
        """
        Return upper http methods name.
        """
        return [force_str(m).upper() for m in cls.http_method_names]

    def write(self, data, status=None, content_type=None, encoder=DjangoJSONEncoder, json_dumps_params=None, **kwargs):
        # status defaults to 200
        return Response(data=data, status=status, content_type=content_type)

    @property
    def data(self):
        """
        Return `request.METHOD`.
        """
        return getattr(self.request, self.request.method)

    @property
    def files(self):
        """
        Return `request.FILES`.
        """
        return getattr(self.request, self.request.FILES)

    @property
    def ip(self):
        request = self.request
        if request.META.get('HTTP_X_FORWARDED_FOR'):
            ip = request.META['HTTP_X_FORWARDED_FOR']
        else:
            ip = request.META['REMOTE_ADDR']
        return ip

    def options(self, request, *args, **kwargs):
        """
        Handles responding to requests for the OPTIONS HTTP verb.
        """
        return_data = {
            "name": self.__class__.__name__,
            "url": self.request.path_info,
            "description": self.__doc__,
            "renders": [
                "application/json",
                "text/html"
            ],
            "parses": [
                "application/json",
                "application/x-www-form-urlencoded",
                "multipart/form-data"
            ]
        }
        return self.write({'return_code': 'success', 'return_data': return_data})
