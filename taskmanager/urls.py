from django.urls import path, include
from rest_framework.routers import DefaultRouter

from rest_framework_nested.routers import NestedDefaultRouter
from .views import ProjectViewSet, TaskViewSet, LoginViewSet, RegisterViewSet, LogoutViewSet, AddUsersToProject

router = DefaultRouter()
router.register(r'auth/login', LoginViewSet, basename='login')
router.register(r'auth/register', RegisterViewSet, basename='register')
router.register(r'auth/logout', LogoutViewSet, basename='logout')
router.register(r'projects', ProjectViewSet)

projects_router = NestedDefaultRouter(router, r'projects', lookup='project')

projects_router.register(
    r'tasks', TaskViewSet,
    basename='tasks',
)
projects_router.register(
    r'add-users-to-project', AddUsersToProject,
    basename='add-users-to-project',
)

urlpatterns = [
    path('', include(router.urls + projects_router.urls)),
]
