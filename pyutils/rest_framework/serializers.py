from django.contrib.auth import get_user_model
from rest_framework import serializers

from pyutils.django.serializers import BaseModelSerializer


User = get_user_model()


class UserSerializer(BaseModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "name",
            "groups",
        ]
