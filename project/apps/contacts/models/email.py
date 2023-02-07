from django.db import models

from .contact import Contact
from apps.contacts.constants import TYPE_MAX_LENGTH, EMAIL_MAX_LENGTH
from apps.contacts.choices import TYPES_OF_EMAIL


class Email(models.Model):
    owner = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name="emails")
    email_addr = models.EmailField(max_length=EMAIL_MAX_LENGTH)
    type = models.CharField(max_length=TYPE_MAX_LENGTH, choices=TYPES_OF_EMAIL)
