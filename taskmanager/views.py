from django.contrib.auth import authenticate

from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from .models import Project, Task
from .permissions import IsProjectOwnerOrReadOnly, IsPartOfThisProject
from .serializers import RegisterSerializer, LoginSerializer, ProjectSerializer, TaskSerializer
from rest_framework import serializers, viewsets, status, mixins


class LoginViewSet(viewsets.ViewSet):
    serializer_class = LoginSerializer
    http_method_names = ['post']

    def create(self, request):
        user = authenticate(email=request.data["email"], password=request.data["password"])
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response(data={"token": token.key, "email": user.email, "profession": user.profession, "id": user.id, "name": user.name},
                            status=status.HTTP_200_OK)
        else:
            return Response(data={"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


class RegisterViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    serializer_class = RegisterSerializer
    http_method_names = ['post']

    def perform_create(self, serializer):
        return serializer.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        token, created = Token.objects.get_or_create(user=user)
        headers = self.get_success_headers(serializer.data)
        serializer.data["token"] = token.key
        return Response(data={"token": token.key, **serializer.data}, status=status.HTTP_201_CREATED, headers=headers)


class LogoutViewSet(viewsets.ViewSet):
    serializer_class = serializers.Serializer()
    permission_classes = [IsAuthenticated]
    http_method_names = ['post']

    def create(self, request):
        user = request.user
        try:
            token = Token.objects.get(user=user)
            token.delete()
            return Response(data={"token": "Token invalidated, successful logout"}, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            return Response(data={"error": "Token not found"}, status=status.HTTP_404_NOT_FOUND)


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, IsProjectOwnerOrReadOnly]
    http_method_names = ['get', 'post', 'put', 'delete', 'head', 'options']

    def get_queryset(self):
        user = self.request.user
        return Project.objects.filter(owner=user)

    def create(self, request, *args, **kwargs):
        request.data['owner'] = request.user.id
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        request.data['owner'] = request.user.id
        return super().update(request, *args, **kwargs)


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsPartOfThisProject]
    http_method_names = ['get', 'post', 'put', 'delete', 'head', 'options']

    def get_queryset(self):
        project_id = self.kwargs['project_pk']
        return Task.objects.filter(project__id=project_id)

    def create(self, request, *args, **kwargs):
        project_id = self.kwargs['project_pk']
        project = get_object_or_404(Project, id=project_id)
        request.data['project'] = project.id
        request.data['created_by'] = request.user.id
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        project_id = self.kwargs['project_pk']
        project = get_object_or_404(Project, id=project_id)
        request.data['project'] = project.id
        request.data['created_by'] = request.user.id
        return super().update(request, *args, **kwargs)
