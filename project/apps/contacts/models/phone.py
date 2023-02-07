from django.db import models

from .contact import Contact
from apps.contacts.constants import PHONE_MAX_LENGTH, TYPE_MAX_LENGTH
from apps.contacts.choices import TYPES_OF_PHONE


class Phone(models.Model):
    owner = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name="phones")
    phone_number = models.CharField(max_length=PHONE_MAX_LENGTH)
    type = models.CharField(max_length=TYPE_MAX_LENGTH, choices=TYPES_OF_PHONE)
