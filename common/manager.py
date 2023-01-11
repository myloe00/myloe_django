from django.db import models
from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from util.common_util import ImmutableDict
from copy import deepcopy
from rest_framework.filters import OrderingFilter
from system.models import SysUser
class REF_obj:
    """
        封装REF参数对象
    """

    def __init__(self, model, serializers_conf=None, views_conf=None):
        self.serializers_conf = serializers_conf or self.DEFAULT_SERIALIZERS_CONF
        self.serializers_conf['model'] = model
        self.views_conf = views_conf or dict()
        self.serializers = type(f"{model.__name__}Serializers", (ModelSerializer, ), {
            "Meta": type("Meta", (), {
                **self.serializers_conf
            })
        })

        self.views_conf['serializer_class'] = self.serializers
        self.views_conf['queryset'] = self.views_conf.get('queryset') or model.objects.all()
        self.views = type(f"{models.__name__}Serializers", (ModelViewSet, ), {**self.views_conf})



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
                "fields": '__all__'
            })
        })
        self._views = type(f"{models.__name__}Serializers", (ModelViewSet,), {
            "serializer_class": self._serializers,
            "filter_backends": (DjangoFilterBackend, OrderingFilter, ),
            "filterset_fields": ['id'],
            "ordering_fields": ['id'],
            "queryset": self.model.objects.all()
        })
        # self.create_views()

    def set_serializers(self, serializers_conf: dict):
        self._serializers.__dict__.update(**serializers_conf)

    def set_views(self, views_conf: dict):
        self._views.__dict__.update(**views_conf)

    def create_views(self):
        ...
        # todo 自定义查询规则

        # todo 排序字段怎么处理

        # todo 分页组件
        # pagination_class
        # todo filterset_fields默认取所有

    @property
    def views(self):
        return self._views


class CURDManager:
    """CURD通用管理器"""

    def __init__(self):
        self._registry = dict()

    def register(self, model, prefix=None, views=None):
        prefix = prefix or model.__name__.lower()
        views = views or ViewsGenerator(model).views
        self._registry[model] = {
            "prefix": prefix, "views": views
        }
        return self

    @property
    def registry(self):
        return self._registry


curd_manager = CURDManager()
curd_manager.register(SysUser)
print("111")
