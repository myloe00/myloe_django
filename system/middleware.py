#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023-01-11 18:00
# @Author  : myloe
# @File    : middleware.py
from common.util.exception import AuthenticationFailed
from common.util.token import JWTToken
from myloe_django.settings import DEBUG


class AuthenticationMiddleware:
    WHITE_LIST = ['/system/login']

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        new_token = None
        if request.path not in self.WHITE_LIST:
            if True:
                token = request.META.get('HTTP_AUTHRIZATION')
                if not token:
                    return AuthenticationFailed('token missing!').json_response
                payloads = JWTToken.decrypt_token(token)
                user = payloads.get('user', dict())
                if not self.valid_user(user):
                    return AuthenticationFailed('The user does not have permissions').json_response
                new_token = JWTToken.refresh_token_by_payloads(payloads)
        response = self.get_response(request)
        if new_token:
            response.headers['Set-Authrization'] = new_token
        return response

    def valid_user(self, user):
        return user
