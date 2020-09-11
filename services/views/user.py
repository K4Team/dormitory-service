# -*- coding: utf-8 -*-
import sys

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status
from rest_framework.views import Response
from services.serializers import UserSerializer
from services.models import SysUser
import json


def get_request_args(func):
    def _get_request_args(self, request):
        if request.method == 'GET':
            args = request.GET
        else:
            body = request.body.decode("utf8")
            if body:
                try:
                    args = json.loads(body)
                except Exception as e:
                    print(e)
                    # return makeJsonResponse(status=StatusCode.EXECUTE_FAIL, message=str(e))
                    args = request.POST
            else:
                args = request.POST
        return func(self, request, args)

    return _get_request_args


class User(viewsets.ViewSet):
    params = [{'name': 'id', 'desc': '参数ID', 'type': openapi.TYPE_INTEGER},
              {'name': 'name', 'desc': '参数name', 'type': openapi.TYPE_STRING},
              {'name': 'title', 'desc': '参数title', 'type': openapi.TYPE_STRING},
              {'name': 'mobile', 'desc': '参数mobile', 'type': openapi.TYPE_STRING},
              {'name': 'email', 'desc': '参数email', 'type': openapi.TYPE_STRING},
              {'name': 'income', 'desc': '参数income', 'type': openapi.TYPE_STRING},
              {'name': 'create_date', 'desc': '参数create_date', 'type': openapi.TYPE_STRING}]

    @swagger_auto_schema(operation_description="获取用户列表", responses={404: 'not found'}, manual_parameters=list(
        openapi.Parameter(i['name'], openapi.IN_QUERY, description=i['desc'], type=i['type']) for i in params))
    def list(self, request):
        data = SysUser.objects.all()
        data_list = UserSerializer(data, many=True)

        return Response(data_list.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(operation_description="获取用户信息",
                         responses={404: 'not found'})
    def retrieve(self, request, pk=None):
        try:
            data = SysUser.objects.get(id=pk)
        except SysUser.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        info = UserSerializer(data)
        return Response(info.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="创建用户",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["name", "title", "email"],
            properties={
                'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                'name': openapi.Schema(type=openapi.TYPE_STRING),
                'title': openapi.Schema(type=openapi.TYPE_STRING),
                'mobile': openapi.Schema(type=openapi.TYPE_STRING),
                'email': openapi.Schema(type=openapi.TYPE_STRING),
                'income': openapi.Schema(type=openapi.TYPE_STRING),
                'create_date': openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        security=[],
        responses={404: 'not found'}
    )
    @get_request_args
    def create(self, request, args):

        a = SysUser.objects.create()
        # for i in args.keys():
        #     a.i
        a.save()
        # a.create_date = self.args['']
        return Response(status=status.HTTP_200_OK)
