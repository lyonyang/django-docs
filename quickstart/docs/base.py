#!/usr/bin/env python
# -*- coding:utf-8 -*-
# __author__ = "lyon"

import inspect
import json
from django.conf import settings
from django.contrib.admindocs.views import simplify_regex
from django.utils.translation import ugettext as _


class ApiEndpoint(object):
    def __init__(self, pattern, method, headers, params, name_parent, desc=None):
        # RegexURLPattern
        self.pattern = pattern
        # http method
        self.method = method
        # callback为view, 由as_view return
        self.callback = pattern.callback
        # self.name = pattern.name
        self.docstring = self.get_doc() or desc
        self.name_parent = name_parent.split('.')[-1]

        if not isinstance(settings.INSTALLED_HANDLERS_NAME, dict):
            raise TypeError(_(
                'settings INSTALLED_HANDLERS_NAME should be dict not %s' % type(settings.INSTALLED_HANDLERS_NAME)))

        alias = settings.INSTALLED_HANDLERS_NAME.get(name_parent) or None
        if alias:
            self.name_parent = alias

        self.path = self.get_path()
        self.methods = [self.method, ]
        self.params = {method: params}
        self.headers = {method: headers}

    def __str__(self):
        return self.docstring

    @property
    def allowed_methods(self):
        methods = []
        for m in self.callback.cls.force_http_method_names():
            if m in self.methods:
                methods.append(m)
        return methods

    @property
    def params_json(self):
        return self.get_params_json(self.params)

    @property
    def headers_json(self):
        return self.get_params_json(self.headers)

    def get_params_json(self, param_dict):
        data = {}
        for method, params in param_dict.items():
            tmp = []
            for p in params:
                tmp.append(p.kwargs)
            data[method] = tmp
        return json.dumps({'data': data})

    def get_path(self):
        return simplify_regex(self.pattern.regex.pattern)

    def get_doc(self):
        return inspect.getdoc(self.callback)


class Param(dict):
    """
    Parameters for building API documents.
    >>> Param('field_name', True, 'type', 'default_value', 'description')
    """

    def __init__(self, field_name, required, param_type, default='', description=''):
        """
        :param field_name: 字段名
        :param required: 是否必填
        :param param_type: 字段值类型, int, str, file
        :param default: 默认值
        :param description: 字段值描述
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
