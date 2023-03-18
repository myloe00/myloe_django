#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023-01-09 15:14
# @Author  : myloe
# @File    : serializers.py
from rest_framework import serializers
from system.models import SysUser, SysRolePermissions, SysRole


def get_easy_serializers(model, fields="__all__"):
    return type(f"{model}Serializers", (serializers.ModelSerializer,), {
        "Meta": type("Meta", (object, ), {
            "model": model,
            "fields": fields
        })
    })()


class SysUserSerializers(serializers.ModelSerializer):
    class Meta:
        model = SysUser
        # fields = ['username', 'first_name', 'last_name']
        fields = '__all__'


class SysRoleModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = SysRole
        fields = "__all__"


class SysRolePermissionsSerializers(serializers.ModelSerializer):
    role = get_easy_serializers(SysRole)

    class Meta:
        model = SysRolePermissions
        fields = "__all__"
