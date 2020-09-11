from rest_framework import serializers
from services import models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SysUser
        fields = "__all__"
