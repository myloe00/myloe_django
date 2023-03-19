from common.util import exception as all_exception

from django.utils.deprecation import MiddlewareMixin

class ExceptionMiddleware(MiddlewareMixin):
    def process_exception(self, request, exception):
        print(" to do ")
