#!/usr/bin/env python
# coding=utf-8
'''
Descripttion: 
Author: myloe
version: 
Date: 2025-04-13 15:33:42
LastEditors: myloe
LastEditTime: 2025-04-13 16:02:55
'''
REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Myloe API',
    'DESCRIPTION': 'Myloe API',
    'VERSION': '1.0.0'
    
}   