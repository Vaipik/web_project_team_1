from uuid import uuid4

from autoslug import AutoSlugField
from django.db import models

from ..libs import constants


class FileCategory(models.Model):
    uuid = models.UUIDField(
        default=uuid4,
        primary_key=True,
        editable=False)
    name = models.CharField(
        max_length=constants.CATEGORY_MAX_LENGTH,
        verbose_name="Category name",
        unique=True
    )
    slug = AutoSlugField(
        populate_from="name",
        max_length=constants.CATEGORY_MAX_URL
    )

    class Meta:
        db_table = "file_storage_categories"
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ["-name"]

    def __str__(self) -> str:
        return self.name

