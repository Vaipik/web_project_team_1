from django.contrib.postgres.fields import ArrayField
from django.db import models

# Create your models here.


# temporary model for testing
class TempNote(models.Model):
    description = models.CharField(max_length=50, null=True, blank=True)
    text = models.CharField(max_length=50, null=True, blank=True)
    tags = ArrayField(models.CharField(max_length=20, null=False, unique=True))


# temporary model for testing
class TempContact(models.Model):
    description = models.CharField(max_length=50, null=True, blank=True)
    text = models.CharField(max_length=50, null=True, blank=True)
    tags = ArrayField(models.CharField(max_length=20, null=False, unique=True))