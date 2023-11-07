from django.contrib.auth import authenticate
from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema

from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView

from .models import Project, Task, MyUser
from .permissions import IsProjectOwnerOrReadOnly, IsPartOfThisProject
from .serializers import RegisterSerializer, LoginSerializer, ProjectSerializer, TaskSerializer
from rest_framework import serializers, viewsets, status, mixins

from .swagger_serializers import AuthResponseSerializer, ProjectResponseSerializer, ProjectPostSerializer, \
    EmailsSerializer


class LoginViewSet(viewsets.ViewSet):
    serializer_class = LoginSerializer
    http_method_names = ['post']

    @swagger_auto_schema(
        query_serializer=LoginSerializer,
        responses={
            '200': AuthResponseSerializer,
            '401': "Unauthorized"
        },
        security=[],
        operation_id='auth_login',
        operation_description="Accepts email and password and returns token that is used for authorization in other endpoints"
    )
    def create(self, request):
        user = authenticate(email=request.data["email"], password=request.data["password"])
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response(data={"token": token.key, "email": user.email, "profession": user.profession, "id": user.id,
                                  "name": user.name},
                            status=status.HTTP_200_OK)
        else:
            return Response(data={"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


class RegisterViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    serializer_class = RegisterSerializer
    http_method_names = ['post']

    def perform_create(self, serializer):
        return serializer.save()

    @swagger_auto_schema(
        query_serializer=RegisterSerializer,
        responses={
            '201': AuthResponseSerializer,
        },
        security=[],
        operation_id='auth_register',
        operation_description="Creates new user and returns token that is used for authorization in other endpoints"
    )
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

    @swagger_auto_schema(
        responses={
            '200': "Token invalidated, successful logout",
            '404': "Token not found",
        },
        operation_id='auth_logout',
        operation_description="Deletes and invalidates users' authorization token"
    )
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
        return Project.objects.filter(Q(owner=user) | Q(other_users=user)).distinct()

    @swagger_auto_schema(
        responses={
            '200': ProjectResponseSerializer(many=True),
        },
        operation_description="Returns all projects that current authed user is part of"
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=ProjectPostSerializer,
        operation_description="Creates new project with current user as owner",
        responses={
            '200': "Success",
        },
    )
    def create(self, request, *args, **kwargs):
        request.data['owner_id'] = request.user.id
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=ProjectPostSerializer,
        operation_description="Updates project",
        responses={
            '200': "Success",
        },
    )
    def update(self, request, *args, **kwargs):
        request.data['owner_id'] = request.user.id
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        responses={
            '200': ProjectResponseSerializer,
        },
        operation_description="Projects details"
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsPartOfThisProject]
    http_method_names = ['get', 'post', 'put', 'delete', 'head', 'options']

    def get_queryset(self):
        project_id = self.kwargs['project_pk']
        return Task.objects.filter(project__id=project_id)

    @swagger_auto_schema()
    def create(self, request, *args, **kwargs):
        project_id = self.kwargs['project_pk']
        project = get_object_or_404(Project, id=project_id)
        request.data['project'] = project.id
        request.data['created_by'] = request.user.id
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema()
    def update(self, request, *args, **kwargs):
        project_id = self.kwargs['project_pk']
        project = get_object_or_404(Project, id=project_id)
        request.data['project'] = project.id
        request.data['created_by'] = request.user.id
        return super().update(request, *args, **kwargs)


class AddUsersToProject(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    http_method_names = ['post']

    @swagger_auto_schema(
        request_body=EmailsSerializer,
        responses={
            '201': "All good, however some emails might have been skipped",
            '404': "Project not found",
            '403': "You're not project's owner",
        },
        operation_description="Accepts list of emails and add those users to project, skips emails not connected to any user"
    )
    def create(self, request, *args, **kwargs):
        emails = request.data.get('emails')
        project_id = self.kwargs['project_pk']
        try:
            project = Project.objects.get(pk=project_id)
            if project.owner_id != request.user.id:
                return Response(data={"error": "You're not project's owner"}, status=status.HTTP_403_FORBIDDEN)

            for email in emails:
                try:
                    user = MyUser.objects.get(email=email.lower())
                    project.other_users.add(user)
                except MyUser.DoesNotExist:
                    print("NOTFOUND:" + email)
            return Response({'message': f'All good {project.name}'}, status=status.HTTP_201_CREATED)
        except Project.DoesNotExist:
            return Response({'error': 'Project not found'}, status=status.HTTP_404_NOT_FOUND)
