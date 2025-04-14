import inspect
import json
from functools import wraps
from rest_framework.decorators import api_view
from django.http.response import JsonResponse as BaseResponse


class JsonResponse(BaseResponse):
    def __init__(self, *args, data=None, code=200, msg='', **kwargs):
        ret_data = {'data': data, 'code': code, 'msg': msg}
        super().__init__(data=ret_data, *args, **kwargs)


def easy_get(func):
    @api_view(['GET'])
    @wraps(func)
    def in_func(request):
        kargs = {}
        tmp_args_name = inspect.getfullargspec(func).args
        for req_param in request.GET.keys():
            if req_param not in tmp_args_name:
                return JsonResponse(data=None, code=400, msg=f'参数{req_param}不存在')
        for key in tmp_args_name:
            kargs[key] = request.GET.get(key, None)
        return func(**kargs)
    return in_func


def easy_post(func):
    @api_view(['POST'])
    @wraps(func)
    def in_func(request):
        kargs = {}
        if request.POST:
            for key in request.POST.keys():
                kargs[key] = request.POST.get(key, None)
        elif request.body:
            try:
                kargs = json.loads(request.body)
            except Exception as e:
                return JsonResponse(data=None, code=400, msg=f'参数错误: {e}')
        tmp_args_name = inspect.getfullargspec(func).args
        for input_param in kargs.keys():
            if input_param not in tmp_args_name:
                return JsonResponse(data=None, code=400, msg=f'未知参数: {input_param}')
        for key in tmp_args_name:
            kargs[key] = kargs.get(key, None)
        return func(**kargs)
    return in_func
