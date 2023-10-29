from django.contrib.auth import authenticate

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Project
from .permissions import IsOwnerOrReadOnlyProject
from .serializers import RegisterSerializer, LoginSerializer, ProjectSerializer
from rest_framework import serializers, viewsets, status, mixins

from rest_framework.authtoken.models import Token


class LoginViewSet(viewsets.ViewSet):
    serializer_class = LoginSerializer

    def create(self, request):
        user = authenticate(email=request.data["email"], password=request.data["password"])
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response(data={"token": token.key}, status=status.HTTP_200_OK)
        else:
            return Response(data={"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


class RegisterViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    serializer_class = RegisterSerializer

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
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnlyProject]

    def get_queryset(self):
        user = self.request.user
        return Project.objects.filter(owner=user)

    def create(self, request, *args, **kwargs):
        request.data['owner'] = request.user.id
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        request.data['owner'] = request.user.id
        return super().update(request, *args, **kwargs)
