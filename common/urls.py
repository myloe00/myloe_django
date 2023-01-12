from django.urls import path
from django.urls.conf import include
# from .views import dispatch_model, UserViews
from rest_framework.routers import DefaultRouter
from .manager import curd_manager, curd_manager_page

router = DefaultRouter()
for model, conf in curd_manager.registry.items():
    router.register(conf['prefix'], conf['views'])

router_page = DefaultRouter()
for model, conf in curd_manager_page.registry.items():
    router_page.register(conf['prefix'], conf['views'])


urlpatterns = [
    # path('easy_curd/<str:app>/<str:model_name>', dispatch_model),
    path('easy_curd/page/', include(router_page.urls)),
    path('easy_curd/', include(router.urls)),
]
