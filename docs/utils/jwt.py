#!/usr/bin/env python
# -*- coding:utf-8 -*-
# __author__ = "lyon"

import datetime
import jwt
from django.conf import settings


class JwtHandler(object):
    @staticmethod
    def get_token(user_id, channel, organ):
        """
        生成Token
        :param data: 一个数据字典,如:{'user_id':1, 'login_time':'2010-01-01 0:0:0'}
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7, seconds=0),  # 过期时间
                'iat': datetime.datetime.utcnow(),  # 发布时间
                'iss': 'ken',  # 发行者
                'data': {
                    'user_id': user_id,
                    'login_time': datetime.datetime.now().strftime("%Y-%m-%D %H:%M:%S")
                }
            }
            # PC
            if str(channel) == settings.PC_CHANNEL:
                secret_key = settings.TOKEN_SECRET_KEY + str(organ)
            # WX
            elif str(channel) == settings.WX_CHANNEL:
                secret_key = settings.WX_TOKEN_SECRET_KEY + str(organ)
            else:
                secret_key = ''
            token = jwt.encode(
                payload,
                secret_key,
                algorithm='HS256'
            )
            return token
        except Exception as e:
            return e

    @staticmethod
    def get_user_id(auth_token, channel, organ):
        """
        验证Token
        :param auth_token:
        :return: integer|string
        """
        try:
            # PC
            if str(channel) == '1':
                # payload = jwt.decode(auth_token, TOKEN_SECRET_KEY, leeway=datetime.timedelta(days=1))
                payload = jwt.decode(auth_token, settings.TOKEN_SECRET_KEY + str(organ))
            # WX
            elif str(channel) == '2':
                # 取消过期时间验证
                payload = jwt.decode(auth_token, settings.WX_TOKEN_SECRET_KEY + str(organ),
                                     options={'verify_exp': False})
            else:
                payload = ''
            if payload:
                return payload['data']['user_id']
            else:
                raise jwt.InvalidTokenError
        except jwt.ExpiredSignatureError:
            # token 过期
            return
        except jwt.InvalidTokenError:
            # token 无效
            return
