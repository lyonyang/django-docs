#!/usr/bin/env python
# -*- coding:utf-8 -*-
# __author__ = "lyon"



def params_check(params):
    from docs.base import Param
    from django.utils.translation import ugettext as _
    if not isinstance(params, (list, tuple)):
        raise TypeError(_('params type must be a list not %s.' % type(params)))
    param_list = []
    for p in params:
        if isinstance(p, tuple):
            param_list.append(Param(*p))
        elif isinstance(p, Param):
            param_list.append(p)
        else:
            raise TypeError(_('api params type %s should be Param  or  tuple not %s.' % (p, type(p).__name__)))
    return param_list
