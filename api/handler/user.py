#!/usr/bin/env python
# -*- coding:utf-8 -*-
# __author__ = "lyon"
import jwt
import datetime
from docs import BaseHandler, api_define
from api.status import CODE, MSG
from django.conf import settings


class SessionLogin(BaseHandler):
    @api_define('session_login', '/session/login', [
        ('username', True, 'str', 'admin', '用户名'),
        ('password', True, 'str', 'admin', '密码'),
    ], desc='用户登录 Session存储')
    def get(self, request):
        username = self.data.get('username')
        password = self.data.get('password')
        if username == 'admin' and password == 'admin':
            self.request.session['user'] = username
        return self.write({'return_code': CODE.SUCCESS, 'return_data': {}})


class JwtLogin(BaseHandler):
    @api_define('jwt_login', '/jwt/login', [
        ('username', True, 'str', 'admin', '用户名'),
        ('password', True, 'str', 'admin', '密码'),
    ], desc='用户登录 Jwt存储')
    def get(self, request):
        username = self.data.get('username')
        password = self.data.get('password')
        if username == 'admin' and password == 'admin':
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7, seconds=0),  # 过期时间
                'iat': datetime.datetime.utcnow(),  # 发布时间
                'iss': 'lyon',  # 发行者
                'data': {
                    'user': username,
                    'login_time': datetime.datetime.now().strftime("%Y-%m-%D %H:%M:%S")
                }
            }
            try:
                token = jwt.encode(
                    payload,
                    settings.secret_key,
                    algorithm='HS256'
                )
            except Exception as e:
                return self.write({'return_code': CODE.FAIL, 'return_msg': MSG.FAIL})
        return self.write({'return_code': CODE.SUCCESS, 'return_data': {'token': token}})
