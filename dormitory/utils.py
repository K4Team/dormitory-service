from datetime import time, datetime
import hashlib
from rest_framework import status
from django.utils.deprecation import MiddlewareMixin
from django_redis import get_redis_connection
from django.http import JsonResponse

r = get_redis_connection()
res = {}


class CheckToken(MiddlewareMixin):

    @staticmethod
    def process_request(request):
        # token验证
        try:
            url = request.path
            if url == "/swagger":
                return
            if url == "/login":
                return
            else:
                token = request.META.get('unique_token')
                if not Token.check_token(token):
                    res['code'] = 401
                    res['message'] = "token已过期，请重新登录！"
                    json_res = JsonResponse(res)
                    json_res.status_code = 401
                    return json_res
                else:
                    return
        except Exception as e:
            print(e)
            res['code'] = 400
            res['message'] = '请求错误!'
            json_res = JsonResponse(res)
            json_res.status_code = 400
            return json_res


class Token:

    @staticmethod
    def create_token(mobile, password):
        token = hashlib.md5(mobile + "-" + password + str(datetime.now())).hexdigest()
        return token

    @staticmethod
    def get_token():
        try:
            store_token = r.get('token')
            if store_token is None:
                return False
            else:
                return store_token
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def check_token(token):
        try:
            old_token = Token.get_token()
            print(old_token)
            if not old_token:
                raise
            if str(old_token, encoding="utf8") != token:
                return False
            return True
        except Exception as e:
            print(e)
            return False
