from django.db import models
from django.contrib.postgres.fields import ArrayField


class Contact(models.Model):
    name = models.CharField(max_length=100, unique=True)
    address = models.CharField(max_length=200)
    email = models.CharField(max_length=100, unique=True)
    birthday = models.DateField()
    phones = ArrayField(models.CharField(max_length=20, unique=True))

    class Meta:
        ordering = ["name"]
