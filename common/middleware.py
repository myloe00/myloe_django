from django.utils.deprecation import MiddlewareMixin


class ExceptionMiddleware(MiddlewareMixin):
    def process_exception(self, request, exception):
        ...
