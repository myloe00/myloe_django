#!/usr/bin/env python
# coding=utf-8
'''
Descripttion: 
Author: myloe
version: 
Date: 2025-04-13 15:57:37
LastEditors: myloe
LastEditTime: 2025-04-13 21:50:52
'''
from django.urls import path
from common.swagger import swagger_demo_view

urlpatterns = [
    path("demo_get/", swagger_demo_view.demo_get),
]
