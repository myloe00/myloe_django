from django.urls import path
from django.urls.conf import include
from rest_framework.routers import DefaultRouter
from .manager import curd_manager, curd_manager_page
from .util import monkey_rest_framework
from django.apps import apps
monkey_rest_framework()



router = DefaultRouter()
for model, conf in curd_manager.registry.items():
    router.register(conf['prefix'], conf['views'])

router_page = DefaultRouter()
for model, conf in curd_manager_page.registry.items():
    router_page.register(conf['prefix'], conf['views'])

app_config = apps.get_app_config("common")

urlpatterns = [
    # todo 关联查询
    path(app_config.batch_route, include(router.urls)),
    path(app_config.page_route, include(router_page.urls)),
    path(app_config.base_route, include(router.urls)),
]
