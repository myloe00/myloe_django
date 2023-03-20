#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023-03-20 16:49
# @Author  : myloe
# @File    : http.py
from django.http.response import JsonResponse as BaseResponse


class JsonResponse(BaseResponse):
    def __init__(self, data=None, code=200, msg='',  *args, **kwargs):
        ret_data = {'data': data, 'code': code, 'msg': msg}
        super().__init__(data=ret_data, *args, **kwargs)


