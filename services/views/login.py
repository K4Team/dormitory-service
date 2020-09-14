# -*- coding: utf-8 -*-
import sys

from django_redis import get_redis_connection
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status
from rest_framework.views import Response
from dormitory.utils import Token
from services.serializers import UserSerializer
from services.models import SysUser
import json
from django.contrib.auth.hashers import check_password
from dormitory.settings import RESPONSE_INFO


r = get_redis_connection()


def get_request_args(func):
    def _get_request_args(self, request, **kwargs):
        if request.method == 'GET':
            args = request.GET
        elif request.method == 'POST' or request.method == "PUT":
            body = request.body.decode("utf8")
            if body:
                try:
                    args = json.loads(body)
                except Exception as e:
                    print(e)
                    if request.method == 'POST':
                        # return makeJsonResponse(status=StatusCode.EXECUTE_FAIL, message=str(e))
                        args = request.POST
                    else:
                        args = request.PUT
            else:
                if request.method == 'POST':
                    # return makeJsonResponse(status=StatusCode.EXECUTE_FAIL, message=str(e))
                    args = request.POST
                else:
                    args = request.PUT
        return func(self, request, args, pk=kwargs['pk'] if "pk" in kwargs.keys() else None)

    return _get_request_args


class Login(viewsets.ViewSet):
    error_info = {'code': 400, 'message': "请求错误，请联系管理员！"}
    success_info = {'code': 200, 'message': '请求成功'}

    @swagger_auto_schema(
        operation_description="登录",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["mobile", "password"],
            properties={
                'mobile': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        security=[],
        responses=RESPONSE_INFO
    )
    @get_request_args
    def create(self, request, args, pk):

        try:
            user = SysUser.objects.filter(mobile=args.mobile).first()
        except Exception as e:
            print(e)
            self.error_info['message'] = "用户名或密码不正确！"
            return Response(self.error_info, status=status.HTTP_400_BAD_REQUEST)
        if check_password(args.password, user.passsword):
            info = UserSerializer(user)
            token = Token.create_token(args.mobile, args.password)
            r.set('token', token, 1800)
            self.success_info['data'] = info.data
            self.success_info['token'] = token
            return Response(self.success_info, status=status.HTTP_200_OK)
        else:
            self.error_info['message'] = "用户名或密码不正确！"
            return Response(self.error_info, status=status.HTTP_400_BAD_REQUEST)
