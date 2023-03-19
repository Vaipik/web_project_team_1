from uuid import uuid4

from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django_celery_beat.models import PeriodicTask


class TaskReminder(models.Model):
    uuid = models.UUIDField(
        default=uuid4,
        primary_key=True,
        editable=False)
    task_name = models.CharField(max_length=64)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    edited_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    senders = models.ManyToManyField("Sender",
                                     through="TaskSender",
                                     through_fields=('task_name', 'sender'),
                                     )
    periodic_tasks = models.ManyToManyField(PeriodicTask,
                                            through="TaskSender",
                                            through_fields=('task_name', 'periodic_task'))

    class Meta:
        verbose_name = 'TaskReminder'
        verbose_name_plural = 'TaskReminders'
        ordering = ['created_at']
        unique_together = ['task_name', 'user']

    def __str__(self) -> str:
        return str(self.task_name)


class Sender(models.Model):
    uuid = models.UUIDField(
        default=uuid4,
        primary_key=True,
        editable=False)
    name = models.CharField(max_length=64, unique=True)
    description = models.CharField(max_length=250)
    model_name = models.CharField(max_length=64, unique=True)

    class Meta:
        verbose_name = 'Sender'
        verbose_name_plural = 'Senders'
        ordering = ['name']

    def __str__(self):
        return str(self.name)


class TaskSender(models.Model):
    uuid = models.UUIDField(
        default=uuid4,
        primary_key=True,
        editable=False)
    task_name = models.ForeignKey(TaskReminder, on_delete=models.CASCADE)
    sender = models.ForeignKey(Sender, on_delete=models.CASCADE, related_query_name="tasksender")
    periodic_task = models.ForeignKey(PeriodicTask, on_delete=models.CASCADE, related_query_name="periodictasks")

    class Meta:
        verbose_name = 'TaskSender'


class SenderSubscription(models.Model):
    uuid = models.UUIDField(
        default=uuid4,
        primary_key=True,
        editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sender = models.ForeignKey(Sender, on_delete=models.CASCADE, related_query_name="subscription")

    class Meta:
        verbose_name = 'SenderSubscription'
        verbose_name_plural = 'SenderSubscriptions'
        ordering = ['user']
        unique_together = ['sender', 'user']

    def __str__(self):
        return str(self.sender.name)
