import logging
from django.views import View
from django.http import HttpResponse
from common.util.http import JsonResponse
from common.util.token import JWTToken
from common.util.exception import AuthenticationFailed
import json
from system.models import SysUser
logger = logging.getLogger("django")


class LoginView(View):

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
        import logging
        logger = logging.getLogger()
        logger.info("INFO!!!!")
        logger.debug("DEBUG!!!!")
        logger.error("ERROR!!!")
        login_data = json.loads(request.body)
        user = SysUser.objects.get(username=login_data.get('username'), password=login_data.get('password'))
        if user:
            token = JWTToken.get_token({"user": user.value})
            # https://blog.csdn.net/qq_31339141/article/details/103888903
            response = JsonResponse()
            response.headers['Set-Authrization'] = token
        else:
            response = AuthenticationFailed.json_response
        return response







