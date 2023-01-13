#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023-01-09 15:14
# @Author  : myloe
# @File    : serializers.py
from rest_framework import serializers
from system.models import SysUser

class SysUserSerializers(serializers.ModelSerializer):
    class Meta:
        model = SysUser
        # fields = ['username', 'first_name', 'last_name']
        fields = '__all__'
