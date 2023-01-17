from django.contrib.auth import get_user_model
from djoser import serializers


class MyUserSerializer(serializers.UserSerializer):
    class Meta:
        model = get_user_model()
        fields = serializers.UserSerializer.Meta.fields + \
        ("first_name", "last_name")