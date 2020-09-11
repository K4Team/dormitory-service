"""dormitory URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from services.views import user
from rest_framework import routers, permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

router = routers.DefaultRouter()
router.register('user', user.User, basename='user')


schema_view = get_schema_view(
    openapi.Info(
        title="系统API",
        default_version='v1.0',
        description="管理系统接口文档",
        terms_of_service="www.baidu.com",
        contact=openapi.Contact(email="1103376617@qq.com"),
        license=openapi.License(name=""),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,)
)

urlpatterns = [
    path('', include(router.urls)),
    path('swagger', schema_view.with_ui('swagger', cache_timeout=0), name='2222'),
    # path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
