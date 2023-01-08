from django.urls import path
from .views import dispatch_model


urlpatterns = [
    path('easy_curd/<str:app>/<str:model_name>', dispatch_model),
]
