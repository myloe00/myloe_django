import logging

from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from util.common_util import ImmutableDict
from rest_framework.filters import OrderingFilter
from .model_config import MyloePagination
from functools import partialmethod
from rest_framework.routers import DefaultRouter

logger = logging.getLogger("django")


def multi_delete(self, request, model, *args, **kwargs):
    """
        批量删除仅支持 in 操作。
        /common/easy_curd/batch/sysuser/?id=1,2,3,4,5
        表示删除id为1，2，3，4，5的5个用户
        # todo 优化返回的描述
    """
    filter_params = dict()
    for key in request.GET.keys():
        filter_params[key+"__in"] = request.GET.get(key).split(",")
    if not filter_params:
        return Response(status=status.HTTP_404_NOT_FOUND)
    model.objects.filter(**filter_params).delete()
    return Response(data={"msg": "delete success"})


def multi_put(self, request, model, *args, **kwargs):
    """
    批量新增
    # todo 返回新增异常的对象
    """
    partial = kwargs.pop('partial', True)
    instances = []
    if isinstance(request.data, list):
        for item in request.data:
            instance = get_object_or_404(model, id=int(item['id']))
            # partial 允许局部更新
            serializer = self.get_serializer(instance, data=item, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
        return Response(data={"msg": "modify success"})
    else:
        raise Exception


def multi_patch(self, request, model, *args, **kwargs):
    kwargs['partial'] = True
    return self.multi_put(request, *args, **kwargs)


def multi_post(self, request, *args, **kwargs):
    headers = None
    if isinstance(request.data, list):
        res = list()
        for item in request.data:
            serializer = self.get_serializer(data=item)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            res.append(serializer.data)
    else:
        raise Exception
    return Response(res, status=status.HTTP_201_CREATED, headers=headers)


class ViewsGenerator:
    DEFAULT_SERIALIZERS_CONF = ImmutableDict({
        "fields": '__all__'
    })

    DEFAULT_VIEWS_CONF = ImmutableDict({
        "filter_backends": (DjangoFilterBackend, OrderingFilter, ),
        "filterset_fields": ['id']
    })

    def __init__(self, model):
        self.model = model
        self._serializers = type(f"{self.model.__name__}Serializers", (ModelSerializer,), {
            "Meta": type("Meta", (), {
                "model": self.model,
                "fields":"__all__"
            })
        })
        self._views = type(f"{self.model.__name__}Serializers", (ModelViewSet, ), {
            "serializer_class": self._serializers,
            "filter_backends": (DjangoFilterBackend, OrderingFilter, ),
            "filterset_fields": "__all__",
            "ordering_fields": ['id'],
            "queryset": self.model.objects.all(),
            "multi_delete": partialmethod(multi_delete, model=self.model),
            "multi_post": partialmethod(multi_post, model=self.model),
            "multi_put": partialmethod(multi_put, model=self.model),
            "multi_patch": partialmethod(multi_patch, model=self.model),
        })
        # self.create_views()

    def config_views(self, views_conf: dict):
        for k, v in views_conf.items():
            setattr(self._views, k, v)

    def set_serializer(self, serializer):
        setattr(self._views, "serializer_class", serializer)

    def set_ordering_fields(self, *args):
        setattr(self._views, args)

    @property
    def views(self):
        return self._views


class CURDManager:
    """CURD通用管理器"""

    def __init__(self):
        self._registry = dict()

    def register(self, model, prefix=None, views=None, with_page=True):
        prefix = prefix or model.__name__.lower()
        views = views or ViewsGenerator(model).views
        if with_page and not getattr(views, "pagination_class"):
            setattr(views, "pagination_class", MyloePagination)
        self._registry[model] = {
            "prefix": prefix, "views": views
        }
        return self

    @property
    def registry(self):
        return self._registry


def register_router(model_config, with_page=False):
    router = DefaultRouter()
    curd_manager = CURDManager()
    for models, config_data in model_config.items():
        prefix = config_data.pop("prefix", None)
        gener = ViewsGenerator(models)
        gener.config_views(config_data)
        curd_manager.register(models, prefix, gener.views, with_page)
    for model, conf in curd_manager.registry.items():
        router.register(conf['prefix'], conf['views'])
    return router

