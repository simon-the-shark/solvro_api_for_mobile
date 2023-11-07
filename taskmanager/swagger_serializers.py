from rest_framework import serializers

from taskmanager.models import MyUser, Project


class AuthResponseSerializer(serializers.ModelSerializer):
    token = serializers.CharField()

    class Meta:
        model = MyUser
        fields = ('token', 'email', 'profession', 'id', 'name')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ('email', 'profession', 'id', 'name')


class ProjectResponseSerializer(serializers.ModelSerializer):
    owner = UserSerializer()
    other_users = UserSerializer(many=True)

    class Meta:
        model = Project
        fields = ('id', 'name', 'owner', 'other_users')



class ProjectPostSerializer(serializers.ModelSerializer):
    other_users_ids = serializers.ListField(child=serializers.PrimaryKeyRelatedField(queryset=MyUser.objects.all()),
                                            required=False, write_only=True)

    class Meta:
        model = Project
        fields = ('id', 'name', 'other_users_ids')


from rest_framework import serializers


class EmailsSerializer(serializers.Serializer):
    emails = serializers.ListField(child=serializers.EmailField())
