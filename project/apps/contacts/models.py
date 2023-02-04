from django.contrib.postgres.fields import ArrayField
from django.db import models

"""
get from feature/contacts branch models.py 
"""


class Contact(models.Model):
    name = models.CharField(max_length=100, unique=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    email = models.CharField(max_length=100, unique=True)
    birthday = models.DateField()
    phones = ArrayField(models.CharField(max_length=20, unique=True))

    class Meta:
        ordering = ["name"]