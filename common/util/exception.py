#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023-03-17 15:05
# @Author  : myloe
# @File    : exception.py
from myloe_django.settings import LOCALE
from django.http import JsonResponse
import logging
logger = logging.getLogger("util")


def translation(msg, locale='zh') -> str:
    resource = LOCALE.get(locale)
    ret = msg
    if resource:
        ret = resource.get(msg, msg)
    return ret


class BaseException(Exception):
    CODE = 1000
    MSG = ''
    dynamic = None

    def __init__(self, msg='', code=None, dynamic=None):
        super().__init__(msg, code)
        self.msg = msg or self.MSG
        if isinstance(dynamic, str):
            self.dynamic = [dynamic]
        else:
            self.dynamic = dynamic
        self.code = code or self.CODE

    def __str__(self):
        try:
            if not self.dynamic:
                self.msg = self.msg.replace('{}', '')
                ret_str = translation(self.msg)
            else:
                ret_str = translation(self.msg).format(*[translation(record) for record in self.dynamic])
        except:
            logger.warning("组织异常信息失败")
            ret_str = translation(self.msg) + ',' + ','.join([translation(record) for record in self.dynamic])
        return ret_str

    @property
    def json_response(self):
        """
            middleware中无法拦截middleware中出现的错误
        """
        return JsonResponse(data={"msg": str(self), "code": self.code}, status=self.code)


class UserFriendlyException(BaseException):
    CODE = 1001


class AuthenticationFailed(BaseException):
    CODE = 401
    MSG = 'Authentication Failed'


if __name__ == '__main__':
    print(UserFriendlyException('this is a test'))
    print(UserFriendlyException('this is test for [{}]'))
    print(UserFriendlyException('this is test for [{}]', dynamic=['myloe']))
