# -*- coding: utf-8 -*-
import sys

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status
from rest_framework.views import Response
from services.serializers import UserSerializer
from services.models import SysUser
import json
import datetime
from django.db import transaction
from django.contrib.auth.hashers import make_password
from dormitory.settings import RESPONSE_INFO
import uuid


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


class User(viewsets.ViewSet):
    params = [{'name': 'id', 'desc': '参数ID', 'type': openapi.TYPE_STRING},
              {'name': 'name', 'desc': '参数name', 'type': openapi.TYPE_STRING},
              {'name': 'password', 'desc': '参数password', 'type': openapi.TYPE_STRING},
              {'name': 'title', 'desc': '参数title', 'type': openapi.TYPE_STRING},
              {'name': 'mobile', 'desc': '参数mobile', 'type': openapi.TYPE_STRING},
              {'name': 'email', 'desc': '参数email', 'type': openapi.TYPE_STRING},
              {'name': 'income', 'desc': '参数income', 'type': openapi.TYPE_STRING},
              {'name': 'create_date', 'desc': '参数create_date', 'type': openapi.TYPE_STRING}]

    error_info = {'code': 400, 'message': "请求错误，请联系管理员！"}
    success_info = {'code': 200, 'message': '请求成功'}

    @swagger_auto_schema(operation_description="获取用户列表", responses=RESPONSE_INFO, manual_parameters=list(
        openapi.Parameter(i['name'], openapi.IN_QUERY, description=i['desc'], type=i['type']) for i in params))
    def list(self, request):
        try:
            data = SysUser.objects.all()
        except Exception as e:
            print(e)
            return Response(self.error_info, status=status.HTTP_400_BAD_REQUEST)
        data_list = UserSerializer(data, many=True)
        self.success_info['data'] = data_list.data
        return Response(self.success_info, status=status.HTTP_200_OK)

    @swagger_auto_schema(operation_description="获取用户信息",
                         responses=RESPONSE_INFO)
    def retrieve(self, request, pk=None):
        try:
            data = SysUser.objects.get(id=pk)
        except Exception as e:
            print(e)
            return Response(self.error_info, status=status.HTTP_400_BAD_REQUEST)
        info = UserSerializer(data)
        self.success_info['data'] = info.data
        return Response(self.success_info, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="创建用户",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["name", "email", "mobile", "password"],
            properties={
                'id': openapi.Schema(type=openapi.TYPE_STRING),
                'name': openapi.Schema(type=openapi.TYPE_STRING),
                'title': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING),
                'mobile': openapi.Schema(type=openapi.TYPE_STRING),
                'email': openapi.Schema(type=openapi.TYPE_STRING),
                'income': openapi.Schema(type=openapi.TYPE_STRING),
                'create_date': openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        security=[],
        responses=RESPONSE_INFO
    )
    @transaction.atomic
    @get_request_args
    def create(self, request, args, pk):

        keys_list = args.keys()
        try:
            SysUser.objects.create(id=uuid.uuid4(), name=args['name'] if 'name' in keys_list else None,
                                   title=args['title'] if 'title' in keys_list else None,
                                   mobile=args['mobile'] if 'mobile' in keys_list else None,
                                   password=make_password(args['password']) if 'password' in keys_list else None,
                                   email=args['email'] if 'email' in keys_list else None,
                                   income=args['income'] if 'income' in keys_list else None,
                                   create_date=datetime.datetime.now())
        except Exception as e:
            print(e)
            return Response(self.error_info, status=status.HTTP_400_BAD_REQUEST)
        return Response(self.success_info, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="编辑用户",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=[],
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING),
                'title': openapi.Schema(type=openapi.TYPE_STRING),
                'mobile': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING),
                'email': openapi.Schema(type=openapi.TYPE_STRING),
                'income': openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        security=[],
        responses=RESPONSE_INFO
    )
    @transaction.atomic
    @get_request_args
    def update(self, request, args, pk):
        try:
            user = SysUser.objects.filter(id=pk).first()
            keys_list = args.keys()
            user.name = args['name'] if 'name' in keys_list else user.name
            user.password = args['password'] if 'password' in keys_list else user.password
            user.title = args['title'] if 'title' in keys_list else user.title
            user.mobile = args['mobile'] if 'mobile' in keys_list else user.mobile
            user.email = args['email'] if 'email' in keys_list else user.email
            user.income = args['income'] if 'income' in keys_list else user.income
            user.save()
        except Exception as e:
            print(e)
            return Response(self.error_info, status=status.HTTP_400_BAD_REQUEST)
        info = UserSerializer(user)
        self.success_info['data'] = info.data
        return Response(self.success_info, status=status.HTTP_200_OK)

    @swagger_auto_schema(operation_description="删除用户信息",
                         responses=RESPONSE_INFO)
    # @action(detail=True, methods=['delete'])
    @transaction.atomic
    def destroy(self, request, pk=None):
        try:
            SysUser.objects.filter(id=pk).first().delete()
        except Exception as e:
            print(e)
            return Response(self.error_info, status=status.HTTP_400_BAD_REQUEST)
        return Response(self.success_info, status=status.HTTP_200_OK)
