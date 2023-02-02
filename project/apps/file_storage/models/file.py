from uuid import uuid4

from django.db import models
from django.conf import settings

from ..libs import constants
from .file_category import Categories


def _get_folder_name(file: str) -> str:
    """Creating folder with name according to category with year, month, day additions"""
    extension = Path(file).suffix[1:]
    for category in Categories:
        if extension in category.value:
            folder_type = category.name
            break
    return f"{folder_type}/%Y/%m/%d"  # Function called after form validation -> folder type 100% will be returned


class File(models.Model):
    uuid = models.UUIDField(
        default=uuid4,
        editable=False,
        primary_key=True
    )
    description = models.CharField(
        max_length=constants.DESCRIPTION_MAX_LENGTH,
        verbose_name="File description",
        blank=True,
        null=True,
    )
    file = models.FileField(
        upload_to=_get_folder_name,
        verbose_name="File path"
    )
    created_at = models.DateTimeField(
        auto_now_add=True
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
        ordering = ["-created_at", ["-name"]]

    def __str__(self) -> str:
        return f"{self.file} | {self.category}"
