from django.db import models
from django.contrib.auth.models import AbstractUser

from taskmanager.user_manager import UserManager


class EstimationChoices(models.IntegerChoices):
    ONE = 1
    TWO = 2
    THREE = 3
    FIVE = 5
    EIGHT = 8
    THIRTEEN = 13
    TWENTY_ONE = 21


class ProfessionChoices(models.TextChoices):
    FRONTEND = "FRONTEND"
    BACKEND = "BACKEND"
    DEVOPS = "DEVOPS"
    UX_UI = "UX/UI", "UX/UI"


class TaskStatusChoices(models.TextChoices):
    NOT_ASSIGNED = "NOT_ASSIGNED"
    IN_PROGRESS = "IN_PROGRESS"
    CLOSED = "CLOSED"


class MyUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    profession = models.CharField(choices=ProfessionChoices.choices, max_length=20)
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class Project(models.Model):
    name = models.CharField(max_length=128, default='<default_name>')
    owner = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name="projects_owned")
    other_users = models.ManyToManyField(MyUser, related_name='projects', blank=True)


class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    created_by = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name="tasks_created_by")
    assigned_to = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name="tasks_assigned", blank=True,
                                    null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=128, default='<default_name>')
    estimation = models.SmallIntegerField(choices=EstimationChoices.choices, )
    status = models.CharField(choices=TaskStatusChoices.choices, max_length=20)
