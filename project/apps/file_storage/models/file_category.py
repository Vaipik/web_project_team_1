from enum import Enum
from uuid import uuid4

from autoslug import AutoSlugField
from django.db import models

from ..libs import constants


class Categories(Enum):
    """Default file categories and their extensions"""
    IMAGES = ("jpeg", "png", "jpg", "svg")
    VIDEOS = ("mp4", "mov", "mkv")
    DOCUMENTS = ("doc", "docx", "txt", "pdf", "xlsx", "pptx")
    AUDIO = ("mp3", "ogg", "wav", "amr")
    ARCHIVES = ("zip", "gz", "tar")


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

