from rest_framework import serializers
from .models import MyUser


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ('email', 'proffesion', 'password')
        extra_kwargs = {'password': {'write_only': True}}


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ('email', 'password')
        extra_kwargs = {'password': {'write_only': True}}
