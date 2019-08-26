#!/usr/bin/env python
# -*- coding:utf-8 -*-
# __author__ = "lyon"

import requests
import json
import functools
from django.http import Http404
from django.views.generic.base import TemplateView
from django.shortcuts import render, redirect
from django.views import View
from django.conf import settings
from django.core.exceptions import DisallowedHost
from django.urls import reverse
from django.http import FileResponse
from . import router


def allowed_host(func):
    def docs_view(self, request, *args, **kwargs):
        if '*' not in settings.DJANGO_DOCS_ALLOWED_HOST:
            if request.META.get('HTTP_X_FORWARDED_FOR'):
                ip = request.META['HTTP_X_FORWARDED_FOR']
            else:
                ip = request.META['REMOTE_ADDR']
            if ip not in settings.DJANGO_DOCS_ALLOWED_HOST:
                raise DisallowedHost("You may need to add '%s' to DOCS_ALLOWED_HOSTS." % ip)
        return func(self, request, *args, **kwargs)

    return docs_view


def hide_check(func):
    @functools.wraps(func)
    def docs_view(*args, **kwargs):
        if settings.DJANGO_DOCS_HIDE:
            if settings.DEBUG:
                raise Http404('API Docs are hidden. Check your settings.')
            raise Http404
        return func(*args, **kwargs)

    return docs_view


class DocsView(TemplateView):
    template_name = 'django_docs/home.html'

    def get_context_data(self, **kwargs):
        context = super(DocsView, self).get_context_data(**kwargs)
        endpoints = router.endpoints

        query = self.request.GET.get("search", "")
        if query and endpoints:
            endpoints = [endpoint for endpoint in endpoints if query in endpoint.path]

        context['query'] = query
        context['endpoints'] = endpoints
        return context

    @hide_check
    @allowed_host
    def get(self, request, *args, **kwargs):
        if not request.session.get('docs_user'):
            return redirect(reverse('django_docs_login'))
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


class LoginDocsView(View):
    @hide_check
    @allowed_host
    def get(self, request):
        return render(request, 'django_docs/login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        if settings.DJANGO_DOCS_PASSWORD:
            if username == settings.DJANGO_DOCS_USERNAME and password == settings.DJANGO_DOCS_PASSWORD:
                request.session['docs_user'] = settings.DJANGO_DOCS_USERNAME
                return redirect(reverse('django_docs_index'))
        else:
            request.session['docs_user'] = settings.DJANGO_DOCS_USERNAME
            return redirect(reverse('django_docs_index'))
        return render(request, 'django_docs/login.html', {'error': 'Incorrect username or password.'})


class LogoutDocsView(View):
    def get(self, request):
        if request.session.get('docs_user'):
            del request.session['docs_user']
        return redirect(reverse('django_docs_login'))


class MarkdownView(View):
    def get(self, request):

        endpoints = {}
        for endpoint in router.endpoints:
            if endpoint.name_parent in endpoints:
                endpoints[endpoint.name_parent].append(endpoint)
            else:
                endpoints[endpoint.name_parent] = [endpoint, ]

        content = ''
        summary = ['- [API文档](#API文档)']
        for k, v in endpoints.items():
            if ord(k[0]) >= 97 and ord(k[0]) <= 122:
                k = k.title
            summary.append('\t' + '- [%s](#%s)' % (k, k))
            content += '## %s\n\n' % k
            for e in v:
                param_markdown_template = "字段名 | 必填 | 类型 | 示例值 | 描述\n:-: | :-: | :-: | :-: | :-:\n"
                for m in e.methods:
                    if m == 'OPTIONS':
                        continue
                    summary.append('\t' * 2 + '- [%s](#%s)' % (e.desc, e.desc))
                    title = "### %s\n\n~%s\n\n%s\n\n" % (e.desc, e.path, m + ' 请求方式\n\n**请求参数**:\n')
                    if e.docstring:
                        title = "### %s\n\n%s\n\n~%s\n\n%s\n\n" % (
                            e.desc, e.docstring, e.path, m + ' 请求方式\n\n**请求参数**:\n')
                    headers = [title, param_markdown_template, ]
                    params = [param_markdown_template, ]
                    request_headers = {}
                    request_params = {}
                    for h in e.headers[m]:
                        headers.append(
                            '%s | %s | %s | %s | %s |\n' % (
                                h.kwargs['field_name'], h.kwargs['required'], h.kwargs['param_type'],
                                h.kwargs['default'], h.kwargs['description']))
                        request_headers[h.kwargs['field_name']] = h.kwargs['default']

                    for p in e.params[m]:
                        params.append(
                            '%s | %s | %s | %s | %s |\n' % (
                                p.kwargs['field_name'], p.kwargs['required'], p.kwargs['param_type'],
                                p.kwargs['default'], p.kwargs['description']))
                        request_params[p.kwargs['field_name']] = p.kwargs['default']
                    if len(headers) == 2:
                        headers = []
                    else:
                        headers.append('\n')
                        headers.insert(1, 'Header\n\n')
                    headers = ''.join(headers)
                    if len(params) == 1:
                        params = []
                    else:
                        params.insert(0, 'Body\n\n')

                    params.append('\n')
                    params = ''.join(params)
                    content += headers + params

                    if hasattr(requests, m.lower()):
                        request_url = '{scheme}://{host}{path}'.format(
                            scheme=request.scheme,
                            host=request._get_raw_host(),
                            path=e.path,
                        )
                        request_func = getattr(requests, m.lower())
                        return_data = request_func(request_url, request_params, headers=request_headers)
                        json_data = json.loads(return_data.text, encoding='utf-8')
                        json_format = json.dumps(json_data, sort_keys=True, indent=4, separators=(',', ':'),
                                                 ensure_ascii=False)
                        content += "请求示例:\n```json\n%s\n```\n\n" % (json_format)

        summary = "<!-- TOC -->\n\n" + "\n".join(summary) + "\n\n<!-- /TOC -->\n\n# API文档\n\n"
        content = summary + content
        response = FileResponse(content)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="django-api-docs.md"'
        return response
