from django.db import models
from django.contrib.auth.models import User


class EstimationChoices(models.IntegerChoices):
    ONE = 1
    TWO = 2
    THREE = 3
    FIVE = 5
    EIGHT = 8
    THIRTEEN = 13
    TWENTY_ONE = 21


class ProffesionChoices(models.TextChoices):
    FRONTEND = "FRONTEND"
    BACKEND = "BACKEND"
    DEVOPS = "DEVOPS"
    UX_UI = "UX/UI"


class TaskStatusChoices(models.TextChoices):
    NOT_ASSIGNED = "NOT_ASSIGNED"
    IN_PROGRESS = "IN_PROGRESS"
    CLOSED = "CLOSED"


class UserProffesion(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profession")
    proffesion = models.CharField(choices=ProffesionChoices.choices, max_length=20)


class Project(models.Model):
    name = models.CharField(max_length=128, blank=True, default='')
    users = models.ManyToManyField(User, related_name='projects')


class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks_created_by")
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks_assigned")
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=128, blank=True, default='')
    estimation = models.SmallIntegerField(choices=EstimationChoices.choices, )
    status = models.CharField(choices=TaskStatusChoices.choices, max_length=20)
