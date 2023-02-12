from django.db import models
from autoslug import AutoSlugField
import uuid
from django.contrib.auth.models import User

from apps.contacts.constants import (
    NAME_MAX_LENGTH,
    ADDRESS_MAX_LENGTH,
    URL_MAX_LENGTH,
    TYPE_MAX_LENGTH,
)
from utils.choices import SEX_CHOICES


class Contact(models.Model):
    """
    Information about a person.
    """

    id = models.UUIDField(
        default=uuid.uuid4,
        primary_key=True,
        editable=False,
    )

    slug = AutoSlugField(
        populate_from="name",
        unique=True,
        max_length=URL_MAX_LENGTH,
        default="",
    )

    owner = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    name = models.CharField(max_length=NAME_MAX_LENGTH, unique=True)
    address = models.CharField(max_length=ADDRESS_MAX_LENGTH, null=True)
    birthday = models.DateField(null=True)
    sex = models.CharField(max_length=TYPE_MAX_LENGTH, choices=SEX_CHOICES, default="u")

    class Meta:
        ordering = ["name"]
