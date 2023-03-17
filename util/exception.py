#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023-03-17 13:46
# @Author  : myloe
# @File    : exception.py

class UserFriendlyException(Exception):
    def __init__(self, message, status):
        super().__init__(message, status)
        self.message = message
        self.status = status