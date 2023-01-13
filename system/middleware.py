#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023-01-11 18:00
# @Author  : myloe
# @File    : middleware.py
from django.http import JsonResponse


class LoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response


