from django.db import models
from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
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


DEFAULT_SERIALIZERS_CONF = {
    "fields": '__all__'
}

DEFAULT_VIEWS_CONF = {
    "filter_backends": (DjangoFilterBackend,),
    "filterset_fields": ['id']
}

def create_views(model, serializers_conf=None, views_conf=None):
    serializers_conf = serializers_conf or DEFAULT_SERIALIZERS_CONF
    serializers_conf['model'] = model
    views_conf = views_conf or DEFAULT_VIEWS_CONF
    serializers = type(f"{model.__name__}Serializers", (ModelSerializer,), {
        "Meta": type("Meta", (), {
            **serializers_conf
        })
    })

    views_conf['serializer_class'] = serializers
    views_conf['queryset'] = views_conf.get('queryset') or model.objects.all()
    views = type(f"{models.__name__}Serializers", (ModelViewSet,), {**views_conf})

    # todo 查询小于怎么处理
    # todo 排序字段怎么处理
    # filterset_fields默认取所有
    return views


class CURDManager:
    """CURD通用管理器"""

    def __init__(self):
        self._registry = dict()

    def register(self, model, prefix=None, views = None):
        prefix = prefix or model.__name__.lower()
        views = views or create_views(model)
        self._registry[model] = {
            "prefix": prefix, "views": views
        }
        return self

    # def register_batch(self, model_list: List[REF_obj]):
    #     [self.register(model) for model in model_list]

    @property
    def registry(self):
        return self._registry


curd_manager = CURDManager()
curd_manager.register(SysUser)
print("111")
