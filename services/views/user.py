# -*- coding: utf-8 -*-
import sys

# from __future__ import unicode_literals
from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.views import APIView
import json
from django.http import JsonResponse
from services.models import SysUser
import datetime

def get_request_args(func):
    def _get_request_args(self, request):
        if request.method == 'GET':
            args = request.GET
        else:
            body = request.body
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


# Create your views here.
class GetOneNews(APIView):
    '''
    list:
        Return one news
    '''
    test_param = openapi.Parameter("id", openapi.IN_QUERY, description="test manual param",
                                   type=openapi.TYPE_INTEGER)

    @swagger_auto_schema(operation_description="partial_update description override",
                         responses={404: 'id not found'},
                         manual_parameters=[test_param])
    @get_request_args
    def get(self, request, args):
        # sql = "SELECT id,name,title,mobile,email,income,create_date FROM sys_user"
        # db = connection.cursor()
        # db.execute(sql)
        #
        # desc = db.description
        #
        # data = list([dict(zip([de[0] for de in desc], row)) for row in db.fetchall()])
        data = SysUser.objects.all()
        print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        data_list = list(data.values())
        # for i in data_list:
        #     i.create_date.
        # dataObject = data.
        return JsonResponse({'data': data_list})

