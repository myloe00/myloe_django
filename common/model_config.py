#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023-01-12 19:29
# @Author  : myloe
# @File    : table_config.py
from system.models import SysUser
from rest_framework.pagination import Response, PageNumberPagination

class MyloePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'page': self.page.number,
            # 'page_size': self.get_page_size(self.request),
            'results': data
        })


model_config = {
    # reference_model:{
    #     # "serializer_class": serializers, 指定序列化对象
    #     # "filter_backends": (DjangoFilterBackend, OrderingFilter,),
    #     # "filterset_fields": ['id'], 定义哪些字段支持搜索
    #     # "ordering_fields": ['id'], 定义排序字段
    #     # "filter_class": ReferenceFilterClass  #自定义过滤条件，使得查询支持大于小于
    #     # "queryset": SysUser.objects.all()
    # },
    SysUser: {} # value为空表示，注册该模型所有配置使用默认配置
}

model_page_config = {
    # reference_model:{
    #     # "serializer_class": serializers, 指定序列化对象
    #     # "filter_backends": (DjangoFilterBackend, OrderingFilter,),
    #     # "filterset_fields": ['id'], 定义哪些字段支持搜索
    #     # "ordering_fields": ['id'], 定义排序字段
    #     # "filter_class": ReferenceFilterClass  #自定义过滤条件，使得查询支持大于小于
    #     # "queryset": SysUser.objects.all()
    #     # "pagination_class": 指定分页器对象
    # },
    SysUser: {} # value为空表示，注册该模型所有配置使用默认配置
}