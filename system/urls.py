#!/usr/bin/env python
# coding=utf-8
'''
Descripttion: 
Author: myloe
version: 
Date: 2025-04-13 13:31:54
LastEditors: myloe
LastEditTime: 2025-04-14 09:51:03
'''
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022-12-07 21:03
# @Author  : myloe
# @File    : urls.py.py
from django.urls import path
from .views import LoginView

urlpatterns = [
    path("login", LoginView.as_view(func='login'))
]
