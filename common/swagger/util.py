import re
import json
import inspect
from typing import get_type_hints
from drf_spectacular.utils import OpenApiParameter, extend_schema, OpenApiTypes, OpenApiExample
from rest_framework.decorators import api_view
from common.util.http import JsonResponse


class AdvanceParams(dict):
    CHOICE = None

    @classmethod
    def extract_example(cls):
        examples = [OpenApiExample(
            name='示例',
            value=cls.extract_value()
        )]
        return examples

    @classmethod
    def extract_value(cls):
        values = dict()
        for k, v in cls.__annotations__.items():
            if isinstance(v, type) and issubclass(v, AdvanceParams):
                v = v.extract_value()
            elif isinstance(v, type):
                v = v.__name__
            values[k] = v
        return values
    
    @classmethod
    def extract_r_value(cls):
        values = dict()
        for k, v in cls.__annotations__.items():
            if isinstance(v, type) and issubclass(v, AdvanceParams):
                v = v.extract_r_value()
                values[k] = {
                    "type": "object",
                    "properties": v
                }
            elif isinstance(v, type):
                values[k] = {
                    "type": "string",
                    "description": v.__name__
                }
            else:
                values[k] = {
                    "type": "string",
                    "description": v
                }
        return values


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


def get_parameters_get(func):
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
        
        description = param_info.get(param_name, f"参数 {param_name}")
        source_type = type_hints.get(param_name, str)
        examples = None
        if source_type == dict:
            param_type = OpenApiTypes.OBJECT
        elif isinstance(source_type, type) and issubclass(source_type, AdvanceParams):
            param_type = OpenApiTypes.OBJECT
            examples = source_type.extract_example()
        else:
            param_type = source_type

        parameters.append(
            OpenApiParameter(
                name=param_name,
                description=description,
                required=param.default == inspect.Parameter.empty,
                enum=None,
                default=param.default if param.default != inspect.Parameter.empty else None,
                type=param_type,
                examples=examples,
            )
        )
    return parameters


def get_parameters_post(func):
    """
    从函数文档中获取参数信息
    :param func: 目标函数
    :return: OpenApiParameter 列表
    """
    type_hints = get_type_hints(func)
    signature = inspect.signature(func)
    properties = {}
    for param_name, _ in signature.parameters.items():
        
        if param_name in ('self', 'cls'):
            continue
        
        source_type = type_hints.get(param_name, str)
        examples = None
        m = {str: 'string', int: 'integer', float: 'number', bool: 'boolean', dict: 'object'}
        param_type = m.get(source_type, source_type)

        if isinstance(param_type, type) and issubclass(param_type, AdvanceParams):
            param_type = 'object'
            examples = source_type.extract_r_value()
            properties[param_name] = {
                'type': param_type,
                'properties': examples,
            }
        else:
            properties[param_name] = {
                'type': param_type,
                'description': examples,
            }
    request_p = {
        "application/json": {
            'type': 'object','properties': properties
        }
    }
    
    return request_p



def easy_api_get(summary=None, description=None, parameters=None, responses=None, **kwargs):
    """
    :param summary: API 摘要
    :param description: API 描述
    :param parameters: API 参数列表
    :param responses: API 响应定义
    :return: 
    """
    def decorator(view_func):
        func_doc = view_func.__doc__
        @extend_schema(
            summary=summary or get_summary_from_doc(func_doc),
            description=description or func_doc,
            parameters=parameters or get_parameters_get(view_func),
            responses=responses or {},
            **kwargs
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


def easy_api_post(summary=None, description=None, request=None, responses=None, **kwargs):
    """
    :param summary: API 摘要
    :param description: API 描述
    :param request: API 请求定义
    :param responses: API 响应定义
    :return: 
    """
    def decorator(view_func):
        func_doc = view_func.__doc__
        
        @extend_schema(
            summary=summary or get_summary_from_doc(func_doc),
            parameters=[
                OpenApiParameter(
                    name='request',
                    description='请求参数',
                    required=True,
                    type='string',
                )
            ],
            description=description or func_doc,
            request=request or get_parameters_post(view_func),
            responses=responses or {},
            **kwargs
        )
        @api_view(['POST'])
        def wrapped_view(request):
            kargs = {}
            if request.body:
                try:
                    kargs = json.loads(request.body)
                except Exception as e:
                    return JsonResponse(data=None, code=400, msg=f'参数错误: {e}')
            tmp_args_name = inspect.getfullargspec(view_func).args
            for input_param in kargs.keys():
                if input_param not in tmp_args_name:
                    return JsonResponse(data=None, code=400, msg=f'未知参数: {input_param}')
            for key in tmp_args_name:
                kargs[key] = kargs.get(key, None)
            return view_func(**kargs)
        return wrapped_view
    return decorator
