#!/usr/bin/env python
# -*- coding:utf-8 -*-
# __author__ = "lyon"

from django.apps import AppConfig


class DocsConfig(AppConfig):
    name = 'docs'
    verbose_name = 'django_api_docs'

    def ready(self):
        from django.conf import settings
        from docs import settings as docs_settings
        def setter_settings(name):
            if not hasattr(settings, name):
                default_settings = getattr(docs_settings, name)
                setattr(settings, name, default_settings)

        for i in dir(docs_settings):
            setter_settings(i)
