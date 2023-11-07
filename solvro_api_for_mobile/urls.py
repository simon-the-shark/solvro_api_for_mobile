"""
URL configuration for solvro_api_for_mobile project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
   openapi.Info(
      title="Taskmanager Demo API",
      default_version='v1',
      description="Simple api for mobile application for student science club recrutation. To authenticate, include token in header in such format: {'Authorization': 'Token 9054f7aa9305e012b3c2300408c3dfdf390fcddf'} Token can be retrieved on /auth/login and /auth/register endpoints.",
      contact=openapi.Contact(email="kontakt@kowalinski.dev"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path("api/", include("taskmanager.urls")),
    path('admin/', admin.site.urls),
]
