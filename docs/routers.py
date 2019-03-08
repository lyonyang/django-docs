#!/usr/bin/env python
# -*- coding:utf-8 -*-
# __author__ = "lyon"

import sys
import six
from importlib import import_module
from django.conf import settings
from docs.doc import ApiEndpoint
from django.core.exceptions import ImproperlyConfigured
from django.contrib.admindocs.views import simplify_regex
from django.utils.encoding import force_str


def import_string(dotted_path):
    """
    Import a dotted module path and return the attribute/class designated by the
    last name in the path. Raise ImportError if the import failed.
    """
    try:
        module_path, class_name = dotted_path.rsplit('.', 1)
    except ValueError:
        msg = "%s doesn't look like a module path" % dotted_path
        six.reraise(ImportError, ImportError(msg), sys.exc_info()[2])

    module = import_module(module_path)

    try:
        return getattr(module, class_name)
    except AttributeError:
        msg = 'Module "%s" does not define a "%s" attribute/class' % (
            module_path, class_name)
        six.reraise(ImportError, ImportError(msg), sys.exc_info()[2])


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
        from django.conf.urls import url
        # 注册api与路由
        if not hasattr(settings, 'INSTALLED_HANDLERS'):
            raise ImproperlyConfigured("The INSTALLED_HANDLERS setting must not be empty.")
        for api in settings.INSTALLED_HANDLERS:
            import_string(api + '.__name__')
        urlpatterns = []
        for module, param in self._registry.items():
            m = import_string(module)
            for p in param:
                func, name, regex, params, headers, desc, display = p['view'], p['name'], p['url'], p[
                    'params'], p['headers'], p['desc'], p['display']
                view_name, method = func.__qualname__.split('.')
                # class
                view = getattr(m, view_name)
                if method not in view.http_method_names:
                    # 不在http_method_names中
                    raise
                method = force_str(method).upper()
                if regex.startswith('/'):
                    regex = regex.replace('/', '', 1)
                pattern = url(r'^%s$' % regex, view.as_view(), name=name)
                urlpatterns.append(pattern)
                if display:
                    for endpoint in self.endpoints:
                        if endpoint.path == simplify_regex(pattern.regex.pattern):
                            endpoint.allowed_methods.append(method)
                            if endpoint.params.get(method):
                                raise
                            else:
                                endpoint.params[method] = params
                                endpoint.headers[method] = headers
                            # TODO url相同
                            break
                    else:
                        self.endpoints.append(
                            ApiEndpoint(pattern=pattern, method=method, headers=headers, params=params,
                                        name_parent=module, desc=desc)
                        )
        return urlpatterns

    @property
    def urls(self):
        if not hasattr(self, '_urls'):
            self._urls = self.get_urls()
        return self._urls


router = Router()
