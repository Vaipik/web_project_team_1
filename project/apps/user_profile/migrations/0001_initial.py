# Generated by Django 4.1.6 on 2023-02-12 06:28

import autoslug.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import utils.file_categories
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Profile",
            fields=[
                (
                    "uuid",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "first_name",
                    models.CharField(max_length=15, verbose_name="First name"),
                ),
                (
                    "last_name",
                    models.CharField(max_length=15, verbose_name="Last name"),
                ),
                ("phone", models.CharField(max_length=20)),
                ("email", models.CharField(max_length=254)),
                (
                    "slug",
                    autoslug.fields.AutoSlugField(
                        editable=False, max_length=20, populate_from="user", unique=True
                    ),
                ),
                (
                    "sex",
                    models.CharField(
                        choices=[("f", "female"), ("m", "male"), ("u", "undefined")],
                        max_length=1,
                        verbose_name="Sex",
                    ),
                ),
                (
                    "avatar",
                    models.ImageField(upload_to=utils.file_categories._get_folder_name),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Profile",
                "verbose_name_plural": "Profiles",
                "db_table": "profiles",
                "ordering": ["first_name", "last_name"],
            },
        ),
    ]