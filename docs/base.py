#!/usr/bin/env python
# -*- coding:utf-8 -*-
# __author__ = "lyon"

"""
API文档构建参数
    Param('user_id', True, 'int', '1', '用户Id')
"""


class Param(dict):
    def __init__(self, field_name, required, param_type, default='', description=''):
        """
        :param field_name: 字段名
        :param required: 是否必须
        :param param_type: 参数类型
        :param default: 默认值
        :param description: 描述
        """
        super(dict, self).__init__()
        self['field_name'] = field_name
        self['required'] = required
        self['param_type'] = param_type
        self['default'] = default
        self['description'] = description

    @property
    def kwargs(self):
        return {
            'field_name': self['field_name'],
            'required': self['required'],
            'param_type': self['param_type'],
            'default': self['default'],
            'description': self['description'],
        }
