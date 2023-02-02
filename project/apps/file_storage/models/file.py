from __future__ import annotations
from pathlib import Path
from uuid import uuid4

from django.db import models
from django.conf import settings

from ..libs import constants
from .file_category import Categories


def _get_folder_name(instance: File, filename) -> str:
    """Creating folder with name according to category with year, month, day additions"""
    extension = Path(filename).suffix[1:]

    for category in Categories:
        if extension in category.value:
            folder_type = category.name
            break

    new_filename = f"{instance.uuid}.{extension}"  # UUID.EXT
    date_path = instance.uploaded_at.date()  # Will be converted in models.FileField
    path = f"{folder_type}/{date_path}/{new_filename}"  # MEDIA/created_date/UUID.EXT
    return path


class File(models.Model):
    uuid = models.UUIDField(
        default=uuid4,
        editable=False,
        primary_key=True
    )
    description = models.CharField(
        max_length=constants.DESCRIPTION_MAX_LENGTH,
        verbose_name="File description",
    )
    # It is IMPORTANT that _uploaded_at_ MUST BE BEFORE _file_ for _get_folder_name function because otherwise
    # it WILL BE NONE
    uploaded_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Uploaded at"
    )
    file = models.FileField(
        upload_to=_get_folder_name,
        verbose_name="File path"
    )
    category = models.ForeignKey(
        to="file_storage.FileCategory",
        on_delete=models.SET_NULL,
        null=True,
        related_name="category"
    )
    owner = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="file"
    )

    class Meta:
        db_table = "file_storage_files"
        verbose_name = "File"
        verbose_name_plural = "Files"
        ordering = ["-category", "-uploaded_at"]

    def __str__(self) -> str:
        return f"{self.file} | {self.category}"
