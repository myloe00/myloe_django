#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023-01-12 18:51
# @Author  : myloe
# @File    : middleware.py
from django.http import JsonResponse


class InterceptPagingRequest:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if "/common/easy_curd/page" in request.path and request.method != "GET":
            return JsonResponse({"msg": f"Method {request.method} not allowed."})
        response = self.get_response(request)
        return response
