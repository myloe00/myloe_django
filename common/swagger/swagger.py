#!/usr/bin/env python
# coding=utf-8
'''
Descripttion: 
Author: myloe
version: 
Date: 2025-04-13 14:06:27
LastEditors: myloe
LastEditTime: 2025-04-13 21:47:32
'''
from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from drf_spectacular.generators import EndpointEnumerator


class BaseEndpointEnumerator(EndpointEnumerator):
    """
    用于过滤API端点。
    """
    OPEN_API = []
    EXCLUDE_PATHS = ['/api/swagger/']

    def should_include_endpoint(self, path, callback):
        include_path = any(path.startswith(p) for p in self.OPEN_API)
        exclude_path = any(path.startswith(p) for p in self.EXCLUDE_PATHS)
        if include_path and not exclude_path:
            return super().should_include_endpoint(path, callback)
        return False


class BaseAPIView(SpectacularAPIView):
    ENDPOINT_INSPECTOR_CLS = BaseEndpointEnumerator
    OPEN_API = []

    def _get_schema_response(self, request):
        self.generator_class.endpoint_inspector_cls = self.ENDPOINT_INSPECTOR_CLS
        self.ENDPOINT_INSPECTOR_CLS.OPEN_API = self.OPEN_API
        return super()._get_schema_response(request)


class DemoSwaggerAPIView(BaseAPIView):
    OPEN_API = ['/api/demo_swagger/']


class OpenApiView(BaseAPIView):
    OPEN_API = ['/api/open_api/']


class AllApiView(BaseAPIView):
    OPEN_API = ['/api/']


urlpatterns = [
    path('all_api/', AllApiView.as_view(), name='all_api'),
    path('all_api/swagger/', SpectacularSwaggerView.as_view(url_name='all_api'), name='all_api_swagger'),
    path('all_api/redoc/', SpectacularRedocView.as_view(url_name='all_api'), name='all_api_redoc'),

    path('demo_swagger/', DemoSwaggerAPIView.as_view(), name='demo_swagger'),
    path('demo_swagger/swagger/', SpectacularSwaggerView.as_view(url_name='demo_swagger'), name='demo_swagger_swagger'),
    path('demo_swagger/redoc/', SpectacularRedocView.as_view(url_name='demo_swagger'), name='demo_swagger_redoc'),

    path('open_api/', OpenApiView.as_view(), name='open_api'),
    path('open_api/swagger/', SpectacularSwaggerView.as_view(url_name='open_api'), name='open_api_swagger'),
    path('open_api/redoc/', SpectacularRedocView.as_view(url_name='open_api'), name='open_api_redoc'),
]
