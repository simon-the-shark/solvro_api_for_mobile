from django.urls import path, include
from rest_framework.routers import DefaultRouter

from taskmanager.views import LoginViewSet, RegisterViewSet, LogoutViewSet

router = DefaultRouter()
router.register(r'auth/login', LoginViewSet, basename='login')
router.register(r'auth/register', RegisterViewSet, basename='register')
router.register(r'auth/logout', LogoutViewSet, basename='logout')

urlpatterns = [
    path('', include(router.urls)),
]
