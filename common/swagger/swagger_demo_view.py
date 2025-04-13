#!/usr/bin/env python
# coding=utf-8
'''
Descripttion: Swagger演示视图
Author: myloe
version: 1.0.0
Date: 2025-04-13 16:00:48
LastEditors: myloe
LastEditTime: 2025-04-13 21:53:28
'''

from common.util.http import JsonResponse
from common.swagger.util import easy_api_get


@easy_api_get()
def demo_get(a:int , b: str, c=10):
    """
    这是一个示例函数

    待实现内容:
    1. json格式的参数
    2. 参数的默认值未实现
    3. return的json数据正确展示暂未实现

    :param a: 参数值a, 查询id, 类型int
    :param b: 参数值b
    :param c: 参数值c
    :return: {'a': a, 'b': b, 'c': c}
    """
    return JsonResponse(data={'a': a, 'b': b, 'c': c})
