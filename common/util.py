#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023-01-13 10:37
# @Author  : myloe
# @File    : util.py

import rest_framework.views
from rest_framework.views import set_rollback
from django.core.exceptions import PermissionDenied
from django.http import Http404

from rest_framework import exceptions, status
from rest_framework.response import Response
from rest_framework.mixins import DestroyModelMixin
from rest_framework.views import View

def exception_handler(exc, context):
    """
    Returns the response that should be used for any given exception.

    By default we handle the REST framework `APIException`, and also
    Django's built-in `Http404` and `PermissionDenied` exceptions.

    Any unhandled exceptions may return `None`, which will cause a 500 error
    to be raised.
    """
    if isinstance(exc, Http404):
        exc = exceptions.NotFound()
    elif isinstance(exc, PermissionDenied):
        exc = exceptions.PermissionDenied()

    if isinstance(exc, exceptions.APIException):
        headers = {}
        if getattr(exc, 'auth_header', None):
            headers['WWW-Authenticate'] = exc.auth_header
        if getattr(exc, 'wait', None):
            headers['Retry-After'] = '%d' % exc.wait

        if isinstance(exc.detail, (list, dict)):
            data = exc.detail
        else:
            data = {'msg': exc.detail}

        set_rollback()
        return Response(data, status=exc.status_code, headers=headers)
    return None

def destroy(self, request, *args, **kwargs):
    instance = self.get_object()
    self.perform_destroy(instance)
    return Response(status=status.HTTP_200_OK, data={"msg": "delete success"})

def dispatch(self, request, *args, **kwargs):
    """
    `.dispatch()` is pretty much the same as Django's regular dispatch,
    but with extra hooks for startup, finalize, and exception handling.
    """
    self.response = View.dispatch(request, *args, **kwargs)
    # self.args = args
    # self.kwargs = kwargs
    # request = self.initialize_request(request, *args, **kwargs)
    # self.request = request
    # self.headers = self.default_response_headers  # deprecate?
    #
    # try:
    #     self.initial(request, *args, **kwargs)
    #
    #     # Get the appropriate handler method
    #     if request.method.lower() in self.http_method_names:
    #         handler = getattr(self, request.method.lower(),
    #                           self.http_method_not_allowed)
    #     else:
    #         handler = self.http_method_not_allowed
    #
    #     response = handler(request, *args, **kwargs)
    #
    # except Exception as exc:
    #     response = self.handle_exception(exc)
    #
    # self.response = self.finalize_response(request, response, *args, **kwargs)
    return self.response


def monkey_rest_framework():
    rest_framework.views.exception_handler = exception_handler
    DestroyModelMixin.destroy = destroy
    View.dispatch = dispatch
