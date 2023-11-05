from django.utils import timezone

from rest_framework import serializers
from .models import MyUser, Project, Task


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ('id', 'email', 'profession', 'password', 'name')
        extra_kwargs = {'password': {'write_only': True}, "id": {"read_only": True}}

    def create(self, validated_data):
        passwrd = validated_data.pop("password")
        user = super().create(validated_data)
        user.set_password(passwrd)
        user.save()
        return user


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ('id', 'email', 'profession', 'password', 'name')
        extra_kwargs = {'password': {'write_only': True}, "profession": {"read_only": True},
                        "name": {"read_only": True}, "id": {"read_only": True}}


class ProjectSerializer(serializers.ModelSerializer):
    other_users = LoginSerializer(many=True, read_only=True)
    other_users_ids = serializers.ListField(child=serializers.PrimaryKeyRelatedField(queryset=MyUser.objects.all()), required=False, write_only=True)
    owner = LoginSerializer(read_only=True)
    owner_id = serializers.PrimaryKeyRelatedField(queryset=MyUser.objects.all(), source='owner', write_only=True)

    class Meta:
        model = Project
        fields = ('id', 'name', 'owner', 'other_users', 'owner_id', "other_users_ids")

    def update(self, instance, validated_data):
        other_users_data = validated_data.pop('other_users_ids', None)
        if other_users_data is not None:
            instance.other_users.set(other_users_data)
        return super().update(instance, validated_data)


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'project', 'created_by', 'assigned_to', 'created_at', 'name', 'estimation', 'status')
    def create(self, validated_data):
        validated_data["created_at"] = timezone.now()
        return super().create(validated_data)