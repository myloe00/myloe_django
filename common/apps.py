from django.apps import AppConfig


class CommonConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'common'
    base_route = 'easy_curd/'
    batch_route = 'easy_curd/batch/'
    page_route = 'easy_curd/page/'

