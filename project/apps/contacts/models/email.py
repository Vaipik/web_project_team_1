from django.db import models

from .contact import Contact
from apps.contacts.constants import TYPE_MAX_LENGTH, EMAIL_MAX_LENGTH
from utils.choices import TYPES_OF_EMAIL


class Email(models.Model):
    """
    Person's email.
    """

    id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name="emails")
    email_addr = models.EmailField(max_length=EMAIL_MAX_LENGTH, blank=True)
    type = models.CharField(max_length=TYPE_MAX_LENGTH, choices=TYPES_OF_EMAIL, blank=True)
