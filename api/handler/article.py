#!/usr/bin/env python
# -*- coding:utf-8 -*-
# __author__ = "lyon"

from docs import Param, BaseHandler, api_define

class ArticleHandler(BaseHandler):
    @api_define('article_list', '/article/list', [
    ], desc='文章列表')
    def get(self, request):
        return self.write({
            'id': 1,
            'title': 'Django-API文档',
            'content': '这是一个能够让我们写接口更快速的工具~'
        })

    @api_define('article_add', '/article/add', [
    ], desc='文章add')
    def post(self, request):
        return self.write({'code':1})