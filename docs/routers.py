#!/usr/bin/env python
# -*- coding:utf-8 -*-
# __author__ = "lyon"

import sys
import six
from importlib import import_module
from django.conf import settings
from docs.doc import ApiEndpoint
from django.core.exceptions import ImproperlyConfigured


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
        for module, params in self._registry.items():
            m = import_string(module)
            for param in params:
                func = param['view']
                name = param['name']
                regex = param['url']
                params = param['params']
                headers = param['headers']
                desc = param['desc']
                view_name, method = func.__qualname__.split('.')
                view = getattr(m, view_name)
                if regex.startswith('/'):
                    regex = regex.replace('/', '', 1)
                pattern = url(r'^%s$' % regex, view.as_view(), name=name)
                urlpatterns.append(pattern)
                self.endpoints.append(
                    ApiEndpoint(pattern=pattern, headers=headers, params=params, name_parent=module, desc=desc)
                )
        print(urlpatterns)
        return urlpatterns

    @property
    def urls(self):
        if not hasattr(self, '_urls'):
            self._urls = self.get_urls()
        return self._urls


router = Router()
