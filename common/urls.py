from django.urls import path
from django.urls.conf import include

from common.easy_curd.manager import register_router
from common.easy_curd.model_config import base_model_config, base_model_config_for_page
from common.easy_curd.monkey_rest_framework import monkey_rest_framework
from django.apps import apps

monkey_rest_framework()


app_config = apps.get_app_config("common")
base_router = register_router(base_model_config)
base_router_for_page = register_router(base_model_config_for_page, with_page=True)


urlpatterns = [
    path(app_config.batch_route, include(base_router.urls)),
    path(app_config.page_route, include(base_router_for_page.urls)),
    path(app_config.base_route, include(base_router.urls)),
]
