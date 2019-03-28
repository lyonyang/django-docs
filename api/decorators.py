#!/usr/bin/env python
# -*- coding:utf-8 -*-
# __author__ = "lyon"
from functools import wraps
from django.conf import settings


# session
def login_required(handler):
    @wraps(handler)
    def _wrapped_view(self, *args, **kwargs):
        if self.request.session.get('user'):
            self.user = self.request.session.get('user')
        else:
            return self.write({'return_code': 'Fail', 'return_msg': 'Unauthorized'})
        return handler(self, *args, **kwargs)

    return _wrapped_view


# jwt
def login_required(handler):
    from functools import wraps
    @wraps(handler)
    def _wrapped_view(self, *args, **kwargs):
        import jwt
        authorization = self.request.META.get('HTTP_AUTHORIZATION') or ' '
        _, token = authorization.split(' ')

        def get_payload():
            try:
                payload = jwt.decode(token, settings.SECRET_KEY, options={'verify_exp': False})
                return payload
            except jwt.ExpiredSignatureError:
                # token 过期
                return
            except jwt.InvalidTokenError:
                # token 无效
                return

        if not get_payload():
            return self.write({'return_code': 'Fail', 'return_msg': 'Unauthorized'})

        # 这里建议你直接设置你的User对象
        # 我的项目中基本都会使用user, user_id, 所以我这里会设置两项
        # self.user = User.objects.filter(username=username).first()
        # self.user = self.user.id
        # 所以在你必须登录的API中, 你可以随意使用self.user, self.user_id
        self.user = get_payload()['data']['user']
        return handler(self, *args, **kwargs)

    return _wrapped_view
