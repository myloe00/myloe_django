from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.http import JsonResponse
from django.apps import apps
from .manager import curd_manager
from rest_framework.viewsets import ModelViewSet
from .serializers import SysUserSerializers
from system.models import SysUser
# 1.导包
from django_filters.rest_framework import DjangoFilterBackend


# 2. 指定查询查询过滤引擎
# Create your views here.

def dispatch_model(request, app, model_name):
    apps.get_registered_model(app, model_name)
    model = apps.get_model(app, model_name)
    #todo 注意并发时的表现
    curd_manager.register(model)
    #todo 引入django-restframework与模型注册
    return JsonResponse({"x": "yes"})

class UserViews(ModelViewSet):
    serializer_class = SysUserSerializers
    queryset = SysUser.objects.all()
    filter_backends = (DjangoFilterBackend,)
    # 指定需要用来进行查询的字段
    filterset_fields = '__all__'

