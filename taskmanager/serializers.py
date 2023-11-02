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

    class Meta:
        model = Project
        fields = ('id', 'name', 'owner', 'other_users')

    # other_user_details = serializers.SerializerMethodField()
    # def get_other_user_details(self, instance):
    #     details = []
    #     other_users = instance.other_users.get_queryset()
    #     for user in other_users:
    #         details.append({"id" : user.id, "email": user.email, "name": user.name, "profession": user.profession})
    #     return details


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'project', 'created_by', 'assigned_to', 'created_at', 'name', 'estimation', 'status')
