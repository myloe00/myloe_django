import re
import inspect
from typing import get_type_hints
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework.decorators import api_view
from common.util.http import JsonResponse


def get_parameter_info(func):
    """
    获取函数的参数信息
    :param func: 目标函数
    :return: 参数信息列表
    """
    signature = inspect.signature(func)
    type_hints = get_type_hints(func)
    parameters = []   
    for name, param in signature.parameters.items():
        if name in ('self', 'cls'):
            continue
            
        param_type = type_hints.get(name, str)
        if hasattr(param_type, '__origin__') and param_type.__origin__ is not None:
            param_type = param_type.__origin__
        
            
        parameters.append(
            OpenApiParameter(
                name=name,
                description=f"参数 {name}",
                required=param.default == inspect.Parameter.empty,
                type=param_type
            )
        )
    return parameters



def get_parameters_from_docstring(docstring):
    """
    从文档字符串中提取参数信息
    :param docstring: 文档字符串
    :return: 参数信息字典
    """
    if not docstring:
        return {}
    
    # 使用正则表达式匹配参数描述
    param_pattern = r':param\s+(\w+):\s*(.*?)(?=\n|$)'
    matches = re.findall(param_pattern, docstring)
    
    # 将匹配结果转换为字典
    param_info = {name: description.strip() for name, description in matches}
    return param_info


def get_summary_from_doc(docstring):
    """
    从函数文档中获取摘要信息
    :param docstring: 文档字符串
    :return: 摘要信息
    """
    if not docstring:
        return ""
    
    # 使用正则表达式匹配 :param 之前的内容
    pattern = r'^(.*?)(?=:param|\Z)'
    match = re.search(pattern, docstring, re.DOTALL)
    
    if match:
        description = match.group(1).strip()
        # 移除多余的空行
        description = re.sub(r'\n\s*\n', '\n', description)
        return description
    return ""


def get_parameters(func):
    """
    从函数文档中获取参数信息
    :param func: 目标函数
    :return: OpenApiParameter 列表
    """
    docstring = func.__doc__
    param_info = get_parameters_from_docstring(docstring)
    type_hints = get_type_hints(func)
    
    parameters = []
    signature = inspect.signature(func)
    for param_name, param in signature.parameters.items():
        
        if param_name in ('self', 'cls'):
            continue
            
        param_type = type_hints.get(param_name, str)
        if hasattr(param_type, '__origin__') and param_type.__origin__ is not None:
            param_type = param_type.__origin__
            
        description = param_info.get(param_name, f"参数 {param_name}")
        _type = type_hints.get(param_name, str)
        parameters.append(
            OpenApiParameter(
                name=param_name,
                description=description,
                required=param.default == inspect.Parameter.empty,
                type=_type
            )
        )
    return parameters



def easy_api_get(summary=None, description=None, parameters=None, responses=None):
    """
    合并 extend_schema 和 easy_get 装饰器的功能
    :param summary: API 摘要
    :param description: API 描述
    :param parameters: API 参数列表
    :param responses: API 响应定义
    :return: 装饰器函数
    """
    def decorator(view_func):
        func_doc = view_func.__doc__
        func_summary = summary or get_summary_from_doc(func_doc)
        func_description = description or func_doc
        func_parameters = parameters or get_parameters(view_func)
        @extend_schema(
            summary=func_summary,
            description=func_description,
            parameters=func_parameters,
            responses=responses or {},
        )
        @api_view(['GET'])
        def wrapped_view(request):
            kargs = {}
            tmp_args_name = inspect.getfullargspec(view_func).args
            for req_param in request.GET.keys():
                if req_param not in tmp_args_name:
                    return JsonResponse(data=None, code=400, msg=f'参数{req_param}不存在')
            for key in tmp_args_name:
                kargs[key] = request.GET.get(key, None)
            return view_func(**kargs)
        return wrapped_view
    return decorator
