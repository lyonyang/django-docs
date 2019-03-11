#!/usr/bin/env python
# -*- coding:utf-8 -*-
# __author__ = "lyon"

from docs import Param, BaseHandler, api_define


class ArticleHandler(BaseHandler):
    @api_define('article_list', '/article/list', [
        Param('get', True, 'str', '1', 'get'),
    ], desc='文章列表')
    def get(self, request):
        return self.write({
            'id': 1,
            'title': 'Django-API文档',
            'content': '这是一个能够让我们写接口更快速的工具~'
        })

    @api_define('article_list', '/article/list', [
        Param('head', True, 'str', '1', 'get')
    ], desc='文章列表')
    def delete(self, request):
        return self.write({
            'id': 1,
            'title': 'Django-API文档',
            'content': '这是一个能够让我们写接口更快速的工具~'
        })

    @api_define('article_list', '/article/list', [
        Param('get', True, 'str', '1', '这个字段1:标识阿豪, 0标识不好中文')
    ], desc='文章列表')
    def post(self, request):
        return self.write({
            'id': 1,
            'title': 'Django-API文档',
            'content': '这是一个能够让我们写接口更快速的工具~'
        })

    @api_define('article_list', '/article/list', [
        Param('get', True, 'str', '1', 'get')
    ], desc='文章列表')
    def put(self, request):
        return self.write({
            'id': 1,
            'title': 'Django-API文档',
            'content': '这是一个能够让我们写接口更快速的工具~'
        })

    @api_define('article_list', '/article/list', [
        Param('get', True, 'str', '1', 'get')
    ], desc='文章列表')
    def patch(self, request):
        return self.write({
            'id': 1,
            'title': 'Django-API文档',
            'content': '这是一个能够让我们写接口更快速的工具~'
        })


    @api_define('article_list', '/article/list', [
        Param('head', True, 'str', '1', 'get')
    ], desc='文章列表')
    def head(self, request):
        return self.write({
            'id': 1,
            'title': 'Django-API文档',
            'content': '这是一个能够让我们写接口更快速的工具~'
        })

    @api_define('article_add', '/article/add', [
        Param('put', True, 'str', '1', 'put'),
        # 'af'
    ], desc='添加文章')
    def put(self, request):
        return self.write({'code': 'put'})

    @api_define('article_add', '/article/add', [
        Param('patch', True, 'str', '1', 'patch')
    ], desc='文章add')
    def patch(self, request):
        return self.write({'code': 'patch'})

    @api_define('article_add', '/article/add', [
        Param('post', True, 'str', '1', 'post')
    ], desc='文章add')
    def post(self, request):
        return self.write({'code': 'post'})
