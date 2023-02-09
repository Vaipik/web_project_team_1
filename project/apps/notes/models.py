from uuid import uuid4

from autoslug import AutoSlugField
from django.db import models
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .libs import constants

User = get_user_model()


# Create your models here.
class Tag(models.Model):
    uuid = models.UUIDField(
        default=uuid4,
        primary_key=True,
        editable=False)
    slug = AutoSlugField(
        populate_from="name",
        max_length=constants.TAG_MAX_URL
    )
    name = models.CharField(max_length=constants.TAG_MAX_LENGTH, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'
        ordering = ['name']

        constraints = [
            models.UniqueConstraint(fields=['user', 'name'], name='tag of username')
        ]

    def __str__(self):
        return self.name


class Note(models.Model):
    uuid = models.UUIDField(
        default=uuid4,
        primary_key=True,
        editable=False)
    slug = AutoSlugField(
        populate_from="name",
        max_length=constants.NOTE_MAX_URL
    )

    name = models.CharField(max_length=constants.NAME_MAX_LENGTH)
    description = models.CharField(max_length=constants.DESCRIPTION_MAX_LENGTH)
    done = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag, related_name='tags_as_note')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Note'
        verbose_name_plural = 'Notes'
        ordering = ['name']

    def __str__(self):
        return self.name
