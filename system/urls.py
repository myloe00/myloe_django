#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022-12-07 21:03
# @Author  : myloe
# @File    : urls.py.py
from django.urls import path
from .views import LoginView

urlpatterns = [
    # todo 功能权限与数据权限该如何隔离？
    path("test", LoginView.as_view(func='login'))
]