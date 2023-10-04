from django.contrib.auth.models import AbstractUser
from django.db import models


class Project(models.Model):
    name = models.CharField(max_length=63, unique=True)
    description = models.TextField(max_length=255)
    image = models.ImageField(upload_to="photo/%Y/%m/%d")

    def __str__(self) -> str:
        return f"{self.name}"


class Team(models.Model):
    name = models.CharField(max_length=63, unique=True)
    description = models.CharField(max_length=127)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="teams")

    def __str__(self) -> str:
        return f"{self.name}, working on {self.project}"


class Position(models.Model):
    name = models.CharField(max_length=63, unique=True)

    def __str__(self) -> str:
        return f"{self.name}"


class Worker(AbstractUser):
    position = models.ForeignKey(Position, on_delete=models.CASCADE, related_name="workers", null=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="workers", null=True)
    image = models.ImageField(upload_to="photo/%Y/%m/%d", blank=True)

    def __str__(self) -> str:
        return f"{self.username} ({self.first_name} {self.last_name})"


class TaskType(models.Model):
    name = models.CharField(max_length=63, unique=True)

    def __str__(self) -> str:
        return f"{self.name}"


class Task(models.Model):
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"
    IMMEDIATE = "immediate"
    PRIORITY_CHOICE = [
        (LOW, LOW),
        (NORMAL, NORMAL),
        (HIGH, HIGH),
        (URGENT, URGENT),
        (IMMEDIATE, IMMEDIATE)
    ]

    name = models.CharField(max_length=63)
    description = models.TextField(max_length=255)
    deadline = models.DateTimeField()
    is_completed = models.BooleanField(default=False)
    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICE,
        default=NORMAL
    )
    task_type = models.ForeignKey(TaskType, on_delete=models.CASCADE, related_name="tasks")
    assignees = models.ManyToManyField(Worker, related_name="tasks")
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="tasks")

    def __str__(self) -> str:
        return f"{self.name}"


class TaskPoint(models.Model):
    name = models.CharField(max_length=63)
    is_done = models.BooleanField(default=False)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="task_points")
