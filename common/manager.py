from django.db import models
from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from util.common_util import ImmutableDict
from rest_framework.filters import OrderingFilter
from .model_config import MyloePagination, model_config, model_batch_config


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
        self._views = type(f"{self.model.__name__}Serializers", (ModelViewSet,), {
            "serializer_class": self._serializers,
            "filter_backends": (DjangoFilterBackend, OrderingFilter, ),
            "filterset_fields": "__all__",
            "ordering_fields": ['id'],
            "queryset": self.model.objects.all()
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

    def register(self, model, prefix=None, views=None):
        prefix = prefix or model.__name__.lower()
        views = views or ViewsGenerator(model).views
        self._registry[model] = {
            "prefix": prefix, "views": views
        }
        return self

    def register_4_page(self, model, prefix=None, views=None):
        prefix = prefix or model.__name__.lower()
        views = views or ViewsGenerator(model).views
        if not getattr(views, "pagination_class"):
            setattr(views, "pagination_class", MyloePagination)
        self._registry[model] = {
            "prefix": prefix, "views": views
        }
        return self

    @property
    def registry(self):
        return self._registry


curd_manager = CURDManager()

for models, config_data in model_config.items():
    prefix = config_data.pop("prefix", None)
    gener = ViewsGenerator(models)
    gener.config_views(config_data)
    curd_manager.register(models, prefix, gener.views)

curd_manager_page = CURDManager()
for models, config_data in model_batch_config.items():
    prefix = config_data.pop("prefix", None)
    gener = ViewsGenerator(models)
    gener.config_views(config_data)
    curd_manager_page.register_4_page(models, prefix, gener.views)
