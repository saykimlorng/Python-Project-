from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import CustomUser


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()  # could be username or email
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if user is None:
            raise serializers.ValidationError("Invalid login credentials.")
        data['user'] = user
        return data
