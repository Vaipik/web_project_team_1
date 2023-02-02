from uuid import uuid4

from django.db import models
from django.conf import settings
from django.utils import timezone

from ..libs import constants


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
        upload_to="%Y/%m/%d"
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
