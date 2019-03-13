#!/usr/bin/env python
# -*- coding:utf-8 -*-
# __author__ = "lyon"

from docs import Param, BaseHandler, api_define
from artilces.models import Article


class ArticleList(BaseHandler):
    @api_define('article_list', '/article/list', headers=[('authorization', False, 'str', '', 'Token'), ], desc='文章列表')
    def get(self, request):
        articles = Article.objects.all().order_by('create_time')
        data = []
        for article in articles:
            data.append(article.serialize())
        return self.write({'return_code': 'success', 'return_data': data})


class ArticleAdd(BaseHandler):
    @api_define('article_add', '/article/add', [
        ('title', True, 'str', 'API Docs', '标题'),
        ('content', True, 'str', '一个构建Web API的工具', '内容'),
        ('author', True, 'str', 'Lyon', '作者'),
    ], [
        ('authorization', False, 'str', '', 'Token'),
    ],desc='添加文章')
    def post(self, request):
        title = self.data.get('title')
        content = self.data.get('content')
        author = self.data.get('author')
        if not all((title, content, author)):
            return self.write({'return_code': 'error', 'return_msg': 'Invalid parameter.'})
        article = Article.objects.create(title=title, content=content, author=author)
        if not article:
            return self.write({'return_code': 'fail', 'return_msg': 'fail'})
        return self.write({'return_code': 'success', 'return_data': {'article_id': article.id}})
