#!/usr/bin/env python
# -*- coding:utf-8 -*-
# __author__ = "lyon"

__title__ = 'Django API Docs'
__version__ = '2.1.2'
__author__ = 'Lyon Yang'

VERSION = __version__

default_app_config = 'django_docs.apps.DjangoDocsConfig'

import sys
import six
import inspect
import json
import functools
from django.conf import settings
from django.conf.urls import url
from importlib import import_module
from django.utils.encoding import force_str
from django.views.decorators.csrf import csrf_exempt
from django.contrib.admindocs.views import simplify_regex
from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe
from .handler import BaseHandler


def import_string(dotted_path):
    """
    Import a dotted module path and return the attribute/class designated by the
    last name in the path. Raise ImportError if the import failed.
    """
    try:
        module_path, class_name = dotted_path.rsplit('.', 1)
    except ValueError:
        module_path, class_name = None, None
        msg = "%s doesn't look like a module path" % dotted_path
        six.reraise(ImportError, ImportError(msg), sys.exc_info()[2])

    module = import_module(module_path)

    try:
        return getattr(module, class_name)
    except AttributeError:
        msg = 'Module "%s" does not define a "%s" attribute/class' % (
            module_path, class_name)
        six.reraise(ImportError, ImportError(msg), sys.exc_info()[2])


def check_param(params):
    if not isinstance(params, (list, tuple)):
        raise TypeError(_('params type must be a list or tuple not %s.' % type(params)))
    param_list = []
    for p in params:
        if isinstance(p, tuple):
            param_list.append(Param(*p))
        elif isinstance(p, Param):
            param_list.append(p)
        else:
            raise TypeError(_('Api params type %s should be Param object or tuple not %s.' % (p, type(p).__name__)))
    return param_list


def docs_define(url, params=None, headers=None, desc='', name=None, display=True):
    """
    :param name: name of reverse generation url
        >>> from django.urls import reverse
        >>> reverse(name)
    :param url: api url
    :param params: request body content
    :param headers: request header content
    :param desc: API description
    :param display: display on the document
    :return:
    """

    if not name:
        name = url.replace('/', '_').strip('_')
    docs_params = settings.DJANGO_DOCS_GLOBAL_PARAMS
    docs_headers = settings.DJANGO_DOCS_GLOBAL_HEADERS

    if params:
        docs_params.extend(list(params))
    if headers:
        docs_headers.extend(list(headers))
    docs_params = check_param(docs_params)
    docs_headers = check_param(docs_headers)

    def decorator(view):
        method = view.__name__
        router.register(view=view, name=name, url=url, params=docs_params,
                        headers=docs_headers,
                        desc=desc, method=method,
                        display=display)

        @functools.wraps(view)
        def handler(*args, **kwargs):
            return view(*args, **kwargs)

        return handler

    return decorator


class Endpoint(object):
    def __init__(self, pattern, method, headers, params, name_parent, desc=None):
        self.pattern = pattern
        self.method = method
        self.callback = pattern.callback
        self.docstring = self.get_doc()
        self.desc = desc
        self.name_parent = name_parent.split('.')[-1].title()
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
        http_method_names = self.callback.view_class.http_method_names
        for m in [force_str(m).upper() for m in http_method_names]:
            if m in self.methods:
                methods.append(m)
        return methods

    def template_method_length(self):
        return len(self.allowed_methods)

    def template_title_length(self):
        return 12 - len(self.allowed_methods)

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
        meta_doc = inspect.getdoc(self.callback)
        if meta_doc:
            return mark_safe(meta_doc.replace('\n', '<br>').replace(' ', '&nbsp;'))
        return meta_doc


class Param(dict):
    """
    Parameters for building API documents.
    >>> Param('field_name', True, 'type', 'default_value', 'description')
    """

    def __init__(self, field_name, required, param_type, default='', description=''):
        """
        :param field_name:
        :param required:
        :param param_type: int, str, file
        :param default:
        :param description:
        """
        super(dict, self).__init__()
        self['field_name'] = field_name
        self['required'] = required
        if not isinstance(param_type, str):
            param_type = param_type.__name__
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


class Router(object):
    def __init__(self):
        self._registry = {}
        self.endpoints = []

    def register(self, **kwargs):
        view = kwargs['view']
        if self._registry.get(view.__module__) is None:
            self._registry[view.__module__] = [kwargs, ]
        else:
            self._registry[view.__module__].append(kwargs)

    def get_urls(self):
        """
        Return a list of URL patterns, given the registered apis.
        """

        for api in settings.INSTALLED_HANDLERS:
            import_string(api + '.__name__')
        urlpatterns = []
        for module, param in self._registry.items():
            m = import_string(module)
            for p in param:
                func, name, regex, params, headers, desc, display = p['view'], p['name'], p['url'], p[
                    'params'], p['headers'], p['desc'], p['display']
                view_name, method = func.__qualname__.split('.')
                # Class
                view = getattr(m, view_name)
                if method not in view.http_method_names:
                    # Method is invalid
                    raise type('HttpMethodError', (Exception,), {})(_('%s is not an HTTP method.' % method))

                method = force_str(method).upper()
                if regex.startswith('/'):
                    regex = regex.replace('/', '', 1)
                pattern = url(r'^%s$' % regex, csrf_exempt(view.as_view()), name=name)
                urlpatterns.append(pattern)
                if display:
                    for endpoint in self.endpoints:
                        if endpoint.path == simplify_regex(pattern.regex.pattern):
                            endpoint.methods.append(method)
                            # Cover if it exists
                            endpoint.params[method], endpoint.headers[method] = params, headers
                            break
                    else:
                        endpoint = Endpoint(pattern=pattern, method=method, headers=headers, params=params,
                                            name_parent=module, desc=desc)
                        if method != "OPTIONS":
                            endpoint.methods.append("OPTIONS")
                            endpoint.params["OPTIONS"], endpoint.headers["OPTIONS"] = [], []
                        self.endpoints.append(endpoint)
        return urlpatterns

    @property
    def urls(self):
        if not hasattr(self, '_urls'):
            self._urls = self.get_urls()
        return self._urls


router = Router()
