#!/usr/bin/env python
# coding=utf-8
'''
Descripttion: Swagger演示视图
Author: myloe
version: 1.0.0
Date: 2025-04-13 16:00:48
LastEditors: myloe
LastEditTime: 2025-04-14 21:20:23
'''

from common.util.http import JsonResponse
from common.swagger.util import easy_api_get, easy_api_post, AdvanceParams


@easy_api_get()
def demo_get(name: str , date: str, size: int = 10):
    """
    这是一个示例函数

    待实现内容:
    2. 参数的默认值未实现
    3. return 数据格式

    :param name: 查询人
    :param date: 查询日期
    :param size: 查询条数
    :return: {'name': name, 'date': date, 'size': size}
    """
    return JsonResponse(data={'name': name, 'date': date, 'size': size})


class School(AdvanceParams):
    name: str
    addr: str


class Person(AdvanceParams):
    name: str
    age: int
    school:  School


@easy_api_post()
def demo_post(name: str, age: int, person: Person):
    """
    这是一个示例函数

    :param name: 姓名
    :param age: 年龄
    :param person: Person对象（dict对象）
    """
    print(name, age, person)
    return JsonResponse(data={'name': name, 'age': age, 'person': person})