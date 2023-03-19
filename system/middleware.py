#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023-01-11 18:00
# @Author  : myloe
# @File    : middleware.py
from django.http import JsonResponse
from common.util.exception import AuthenticationFailed


class AuthenticationMiddleware:
    WHITE_LIST = ['/system/login']

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path not in self.WHITE_LIST:
            res = self.valid_user(request)
            if res:
                return res
        self.update_user(request)
        response = self.get_response(request)
        return response

    def valid_user(self, request):
        token = request.META.get('HTTP_AUTHENTICATION', '')
        if not token:
            return AuthenticationFailed().json_response
        # 验证token

    def update_user(self, request):
        # todo 加载redis中的内容
        user = request.user

    def process_exception(self, request, exception):

        print(
            "xxxxxxxxxx222"
        )
