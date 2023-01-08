from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.http import JsonResponse
from django.apps import apps
from .manager import curd_manager

# Create your views here.

def dispatch_model(request, app, model_name):
    apps.get_registered_model(app, model_name)
    model = apps.get_model(app, model_name)
    #todo 注意并发时的表现
    curd_manager.register(model)
    #todo 引入django-restframework与模型注册
    return JsonResponse({"x": "yes"})
