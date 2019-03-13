#!/usr/bin/env python
# -*- coding:utf-8 -*-
# __author__ = "lyon"

from docs import Param, BaseHandler, api_define
from apps.articles.models import Article
from api.status import CODE, MSG


class ArticleList(BaseHandler):
    @api_define('article_list', '/article/list', desc='文章列表')
    def get(self, request):
        articles = Article.objects.all().order_by('create_time')
        data = []
        for article in articles:
            data.append(article.serializ)
        return self.write({'return_code': CODE.SUCCESS, 'return_data': data})

class ArticleAdd(BaseHandler):
    @api_define('article_add', '/article/add', [
        Param('title', True, 'str', 'API Docs', '标题'),
        Param('content', True, 'str', '一个构建Web API的工具', '内容'),
        Param('author', True, 'str', 'Lyon', '作者'),
    ], desc='添加文章')
    def post(self, request):
        title = self.data.get('title')
        content = self.data.get('content')
        author = self.data.get('author')
        if not all((title, content, author)):
            return self.write({'return_code': CODE.INVALID_PARAMETER, 'return_msg': MSG.INVALID_PARAMETER})
        article = Article.create_data(title=title, content=content, author=author)
        if not article:
            return self.write({'return_code': CODE.FAIL, 'return_msg': MSG.FAIL})
        return self.write({'return_code': CODE.SUCCESS, 'return_data': {}})


class ArticleDelete(BaseHandler):
    @api_define('article_delete', '/article/delete', [
        Param('article_id', True, 'int', '1', '文章ID'),
    ], desc='删除文章')
    def post(self, request):
        article_id = self.data.get('article_id')
        article = Article.objects.filter(id=article_id).first()
        if not article:
            return self.write({'return_code': CODE.INVALID_PARAMETER, 'return_msg': MSG.INVALID_PARAMETER})

        flag = Article.delete_data(article)
        if not flag:
            return self.write({'return_code': CODE.FAIL, 'return_msg': MSG.FAIL})
        return self.write({'return_code': CODE.SUCCESS, 'return_data': {'article_id': article_id}})


class ArticleEdit(BaseHandler):
    @api_define('article_edit', '/article/edit', [
        Param('article_id', True, 'int', '1', '文章ID'),
        Param('title', True, 'str', 'API Docs', '标题'),
        Param('content', True, 'str', '一个构建Web API的工具', '内容'),
        Param('author', True, 'str', 'Lyon', '作者'),
    ], desc='编辑文章')
    def post(self, request):
        article_id = self.data.get('article_id')
        title = self.data.get('title')
        content = self.data.get('content')
        author = self.data.get('author')
        if not all((title, content, author)):
            return self.write({'return_code': CODE.INVALID_PARAMETER, 'return_msg': MSG.INVALID_PARAMETER})
        article = Article.objects.filter(id=article_id).first()
        if not article:
            return self.write({'return_code': CODE.INVALID_PARAMETER, 'return_msg': MSG.INVALID_PARAMETER})

        flag = Article.edit_data(article, title, content, author)
        if not flag:
            return self.write({'return_code': CODE.FAIL, 'return_msg': MSG.FAIL})
        return self.write({'return_code': CODE.SUCCESS, 'return_data': {'article_id': article_id}})
