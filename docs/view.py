#!/usr/bin/env python
# -*- coding:utf-8 -*-
# __author__ = "lyon"

from django.http import Http404
from django.views.generic.base import TemplateView
from django.shortcuts import render, redirect
from django.views import View
from django.conf import settings
from django.core.exceptions import DisallowedHost


def host_is_allowed(request):
    if '*' not in settings.DOCS_ALLOWED_HOSTS:
        if request.META.get('HTTP_X_FORWARDED_FOR'):
            ip = request.META['HTTP_X_FORWARDED_FOR']
        else:
            ip = request.META['REMOTE_ADDR']
        if ip not in settings.DOCS_ALLOWED_HOSTS:
            raise DisallowedHost("You may need to add '%s' to DOCS_ALLOWED_HOSTS." % ip)


class DocsView(TemplateView):
    template_name = "docs/home.html"

    def get_context_data(self, **kwargs):
        from docs.routers import router
        context = super(DocsView, self).get_context_data(**kwargs)
        endpoints = router.endpoints

        query = self.request.GET.get("search", "")
        if query and endpoints:
            endpoints = [endpoint for endpoint in endpoints if query in endpoint.path]

        context['query'] = query
        context['endpoints'] = endpoints
        return context

    def get(self, request, *args, **kwargs):
        if settings.HIDE_API_DOCS:
            raise Http404("API Docs are hidden. Check your settings.")

        host_is_allowed(request)

        if not request.session.get('user'):
            return redirect('/docs/login')
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


class LoginDocsView(View):
    def get(self, request):
        if settings.HIDE_API_DOCS:
            raise Http404("API Docs are hidden. Check your settings.")

        host_is_allowed(request)

        return render(request, 'docs/login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username == settings.DOCS_USERNAME and password == settings.DOCS_PASSWORD:
            request.session['user'] = settings.DOCS_USERNAME
            return redirect('/docs')
        return render(request, 'docs/login.html', {'error': 'Incorrect username or password.'})


class LogoutDocsView(View):
    def get(self, request):
        if request.session.get('user'):
            del request.session['user']
        return redirect("/docs/login/")
