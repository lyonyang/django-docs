#!/usr/bin/env python
# -*- coding:utf-8 -*-
# __author__ = "lyon"

from django.conf import settings
from django.utils.translation import ugettext as _
from . import settings as docs_settings
from .base import Param


def params_check(params):
    if not isinstance(params, (list, tuple)):
        raise TypeError(_('params type must be a list or tuple not %s.' % type(params)))
    param_list = []
    for p in params:
        if isinstance(p, tuple):
            param_list.append(Param(*p))
        elif isinstance(p, Param):
            param_list.append(p)
        else:
            raise TypeError(_('api params type %s should be Param or tuple not %s.' % (p, type(p).__name__)))
    return param_list


def settings_check():
    for s in dir(docs_settings):
        if not hasattr(settings, s):
            setting_value = getattr(docs_settings, s)
            setattr(settings, s, setting_value)
