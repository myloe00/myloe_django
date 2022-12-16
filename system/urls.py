#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022-12-07 21:03
# @Author  : myloe
# @File    : urls.py.py
from django.urls import path
from .views import LoginView

urlpatterns = [
    path("test", LoginView.as_view(func='login'))
]