from django.contrib import admin

from taskmanager.models import UserProffesion, Project, Task

# Register your models here.
admin.site.register(UserProffesion)
admin.site.register(Project)
admin.site.register(Task)