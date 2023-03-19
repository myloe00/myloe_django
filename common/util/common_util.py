#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023-01-10 10:37
# @Author  : myloe
# @File    : common_util.py

class ImmutableDict(dict):
    def __setitem__(self, key, value):
        raise TypeError("immutable dict can not be modified !")

    def __delattr__(self, item):
        raise SystemError("immutable dict can not be modified !")

    @property
    def copy(self):
        return {k: v for k, v in self.items()}
