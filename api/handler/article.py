#!/usr/bin/env python
# -*- coding:utf-8 -*-
# __author__ = "lyon"

from docs import Param, BaseHandler, api_define
from apps.articles.models import Article


class ArticleList(BaseHandler):
    @api_define('article_list', '/article/list', desc='文章列表')
    def get(self, request):
        return self.write({'return_code': 'success', 'return_data': {}})


class ArticleAdd(BaseHandler):
    @api_define('article_add', '/article/add', [
        Param('title', True, 'str', 'API Docs', '标题'),
        Param('content', True, 'str', '一个构建Web API的工具', '内容'),
    ], desc='添加文章')
    def post(self, request):
        return self.write({'return_code': 'success', 'return_data': {}})


class ArticleDelete(BaseHandler):
    @api_define('article_delete', '/article/delete', [
    ], desc='删除文章')
    def post(self, request):
        return self.write({'return_code': 'success', 'return_data': {}})


class ArticleEdit(BaseHandler):
    @api_define('article_edit', '/article/edit', [
    ], desc='编辑文章')
    def post(self, request):
        return self.write({'return_code': 'success', 'return_data': {}})


class ArticleDetail(BaseHandler):
    @api_define('article_detail', '/article/detail', [
    ], desc='文章详情')
    def post(self, request):
        return self.write({'return_code': 'success', 'return_data': {}})
