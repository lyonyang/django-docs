#!/usr/bin/env python
# -*- coding:utf-8 -*-
# __author__ = "lyon"

from django.conf import settings
from django.apps import AppConfig
from django.utils.translation import ugettext as _
from . import router, default, import_string



class DjangoDocsConfig(AppConfig):
    name = 'django_docs'

    def ready(self):
        self.setup()
        urlpatterns = import_string(settings.ROOT_URLCONF + '.urlpatterns')
        urlpatterns += router.urls

    def setup(self):
        for name in dir(default):
            if not name.startswith('__') and not hasattr(settings, name):
                setattr(settings, name, getattr(default, name))

        if not isinstance(settings.INSTALLED_HANDLERS, (list, tuple)):
            raise TypeError(_(
                'settings INSTALLED_HANDLERS should be list not %s' % type(settings.INSTALLED_HANDLERS)))

        if not isinstance(settings.INSTALLED_HANDLERS_NAME, dict):
            raise TypeError(_(
                'settings INSTALLED_HANDLERS_NAME should be dict not %s' % type(settings.INSTALLED_HANDLERS_NAME)))
