from django.contrib import admin

from taskmanager.models import MyUser, Project, Task

# Register your models here.
admin.site.register(MyUser)
admin.site.register(Project)
admin.site.register(Task)