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
from django.utils.translation import ugettext as _
from django.views import View
from docs import settings as docs_settings


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

        if not hasattr(settings, 'INSTALLED_HANDLERS_NAME'):
            setattr(settings, 'INSTALLED_HANDLERS_NAME', docs_settings.INSTALLED_HANDLERS_NAME)
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
        sorted_method = []
        for m in self.callback.cls.http_method_names:
            if m.upper() in self.methods:
                sorted_method.append(force_str(m).upper())
        return sorted_method

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


class DocsView(TemplateView):
    template_name = "docs/home.html"

    def get_context_data(self, **kwargs):
        from docs.routers import router
        if hasattr(settings, 'HIDE_API_DOCS'):
            setattr(settings, 'HIDE_API_DOCS', docs_settings.HIDE_API_DOCS)
        if not settings.HIDE_API_DOCS:
            raise Http404("API Docs are hidden. Check your settings.")

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
        if username == 'admin' and password == 'docs':
            request.session['user'] = 'admin'
            return redirect('/docs')
        return render(request, 'docs/login.html', {'error': 'Incorrect username or password.'})


class LogoutDocsView(View):
    def get(self, request):
        if request.session.get('user'):
            del request.session['user']
        return redirect("/docs/login/")
