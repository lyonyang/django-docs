#!/usr/bin/env python
# -*- coding:utf-8 -*-
# __author__ = "lyon"

__title__ = 'django-apidocs'
__version__ = '1.0.0'
__author__ = 'Lyon'
__license__ = 'Apache License Version 2.0'
__copyright__ = 'Copyright 2018 Lyon Yang'

VERSION = __version__

from docs.routers import router
from docs.view import DocsView, LoginDocsView, LogoutDocsView
from docs.base import Param, ApiEndpoint
from docs.handler import BaseHandler
from django_docs.decorators import api_define, login_required
from docs.urls import urlpatterns

__all__ = [
    'router', 'BaseHandler', 'api_define',
    'login_required', 'Param', 'DocsView',
    'LoginDocsView', 'LogoutDocsView', 'urlpatterns',
    'ApiEndpoint',
]
