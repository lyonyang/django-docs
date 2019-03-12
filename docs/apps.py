#!/usr/bin/env python
# -*- coding:utf-8 -*-
# __author__ = "lyon"

from django.apps import AppConfig
from django.conf import settings


class DocsConfig(AppConfig):
    name = 'docs'

    def ready(self):
        from docs import settings as docs_settings

        def setter_settings(name):
            if not hasattr(settings, name):
                default_settings = getattr(docs_settings, name)
                setattr(settings, name, default_settings)

        for i in dir(docs_settings):
            setter_settings(i)
