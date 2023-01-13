from django.urls import path
from django.urls.conf import include
from rest_framework.routers import DefaultRouter
from .manager import curd_manager, curd_manager_page
from .util import monkey_rest_framework
monkey_rest_framework()

router = DefaultRouter()
for model, conf in curd_manager.registry.items():
    router.register(conf['prefix'], conf['views'])

router_page = DefaultRouter()
for model, conf in curd_manager_page.registry.items():
    router_page.register(conf['prefix'], conf['views'])


urlpatterns = [
    # todo 批量修改测试验证
    # todo 关联查询
    path('easy_curd/page/', include(router_page.urls)),
    path('easy_curd/batch/', include(router.urls)),
    path('easy_curd/', include(router.urls)),
]
