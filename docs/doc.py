#!/usr/bin/env python
# -*- coding:utf-8 -*-
# __author__ = "lyon"

import inspect
import json
from django.conf import settings
from django.contrib.admindocs.views import simplify_regex
from django.http import Http404
from django.utils.encoding import force_str
from django.views.generic.base import TemplateView
from django.shortcuts import render, redirect
from django.views import View


class ApiEndpoint(object):
    def __init__(self, pattern, headers, params, name_parent, desc=None):
        # RegexURLPattern 对象
        self.pattern = pattern
        # view
        self.callback = pattern.callback
        # self.name = pattern.name
        self.docstring = self.get_doc() or desc
        self.name_parent = name_parent.split('.')[-1]
        if hasattr(settings, "INSTALLED_HANDLERS_NAME"):
            alias = settings.INSTALLED_HANDLERS_NAME.get(name_parent) or None
            if alias:
                self.name_parent = alias
        self.path = self.get_path()
        self.allowed_methods = self.get_allowed_methods()
        # self.view_name = pattern.callback.__name__
        self.params = params
        self.headers = headers
        self.params_json = self.get_params_json(self.params)
        self.headers_json = self.get_params_json(self.headers)

    def get_params_json(self, params):
        data = []
        for p in params:
            data.append(p.kwargs)
        return json.dumps({'data': data})

    def get_path(self):
        return simplify_regex(self.pattern.regex.pattern)

    def is_method_allowed(self, callback_cls, method_name):
        return hasattr(callback_cls, method_name)

    def get_allowed_methods(self):
        view_methods = [force_str(m).upper()
                        for m in self.callback.cls.http_method_names
                        if self.is_method_allowed(self.callback.cls, m)]
        return sorted(view_methods)

    def get_doc(self):
        return inspect.getdoc(self.callback)


class DRFSettings(object):
    def __init__(self):
        self.drf_settings = {
            "HIDE_DOCS": self.get_setting("HIDE_DOCS") or False
        }

    def get_setting(self, name):
        try:
            return settings.REST_FRAMEWORK_DOCS[name]
        except:
            return None

    @property
    def settings(self):
        return self.drf_settings


class DocsView(TemplateView):
    template_name = "docs/home.html"

    def get_context_data(self, **kwargs):
        from docs.routers import router
        settings = DRFSettings().settings
        if settings["HIDE_DOCS"]:
            raise Http404("Django Rest Framework Docs are hidden. Check your settings.")

        context = super(DocsView, self).get_context_data(**kwargs)
        endpoints = router.endpoints

        query = self.request.GET.get("search", "")
        if query and endpoints:
            endpoints = [endpoint for endpoint in endpoints if query in endpoint.path]

        context['query'] = query
        context['endpoints'] = endpoints
        return context

    def get(self, request, *args, **kwargs):
        if not request.session.get('user'):
            return redirect('/docs/login')
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


class LoginDocsView(View):
    def get(self, request):
        return render(request, 'docs/login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username == 'admin' and password == 'lyondjangoapi':
            request.session['user'] = 'admin'
            return redirect('/docs')
        return render(request, 'docs/login.html', {'error': '用户名或密码错误'})


class LogoutDocsView(View):
    def get(self, request):
        if request.session.get('user'):
            del request.session['user']
        return redirect("/docs/login/")
