from django.db import models


class Contact(models.Model):
    name = models.CharField(max_length=100, unique=True)
    address = models.CharField(max_length=200)
    email = models.CharField(max_length=100, unique=True)
    birth_date = models.DateTimeField()


class Phone(models.Model):
    phone_number = models.CharField(max_length=20)
    owner = models.ForeignKey(Contact, on_delete=models.CASCADE)
