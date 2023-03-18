import logging
import time

from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
logger = logging.getLogger("django")

from django.views import View

class LoginView(View): #需要继承自View类

    func = ''

    def dispatch(self, request, *args, **kwargs):
        if hasattr(self, self.func):
            handler = getattr(self, self.func)
        else:
            handler = getattr(self, request.method.lower(), self.http_method_not_allowed)

        return handler(request, *args, **kwargs)

    def get(self, request):
        return HttpResponse("登录成功")

    def login(self, request):
        # https: // blog.csdn.net / qq_31339141 / article / details / 103888903
        return HttpResponse("登录成功2")



