#!/usr/bin/env python
# -*- coding:utf-8 -*-
# __author__ = "lyon"
"""
API 文档URLS :
    url(r'^$', csrf_exempt(DocsView.as_view())),
    url(r'^login/$', csrf_exempt(LoginDocsView.as_view())),
    url(r'^logout/$', csrf_exempt(LogoutDocsView.as_view())),
"""

from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
from docs.view import DocsView, LoginDocsView, LogoutDocsView, MarkdownView

urlpatterns = [
    url(r'^$', csrf_exempt(DocsView.as_view())),
    url(r'^login/$', csrf_exempt(LoginDocsView.as_view())),
    url(r'^logout/$', csrf_exempt(LogoutDocsView.as_view())),
    url(r'^markdown/$', csrf_exempt(MarkdownView.as_view()), name='markdown'),
]
