from uuid import uuid4

from django.contrib.auth.models import User
from django.db import models


class TelegramChat(models.Model):
    uuid = models.UUIDField(
        default=uuid4,
        primary_key=True,
        editable=False)
    chat_id = models.IntegerField(unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'TelegramChat'
        verbose_name_plural = 'TelegramChats'
        ordering = ['user']


# TODO add telegram registration page