from uuid import uuid4

from autoslug import AutoSlugField
from django.db import models
from django.contrib.auth.models import User
from PIL import Image

from .libs import constants
from utils.file_categories import _get_folder_name
from utils.choices import SEX_CHOICES


class Profile(models.Model):
    uuid = models.UUIDField(
        default=uuid4,
        primary_key=True,
        editable=False
    )
    first_name = models.CharField(
        max_length=constants.FIRSTNAME_MAX_LENGTH,
        verbose_name="First name",
        default=None,
        null=True
    )
    last_name = models.CharField(
        max_length=constants.LASTNAME_MAX_LENGTH,
        verbose_name="Last name",
        default=None,
        null=True
    )
    phone = models.CharField(
        max_length=constants.PHONE_MAX_LENGTH,
        verbose_name="phone number",
        default=None,
        blank=True,
        null=True
    )
    email = models.CharField(
        max_length=constants.EMAIL_MAX_LENGTH,
        verbose_name="email address",
        default=None,
        blank=True,
        null=True
    )
    slug = AutoSlugField(
        populate_from="username",
        unique=True,
        max_length=constants.PROFILE_MAX_URL
    )
    sex = models.CharField(
        max_length=1,
        choices=SEX_CHOICES,
        verbose_name="Sex",
        default="u"
    )
    avatar = models.ImageField(
        upload_to=_get_folder_name,
        default=constants.DEFAULT_AVATAR_URL,
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        db_table = "user_profiles"
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"
        ordering = ["first_name", "last_name"]

    def __str__(self) -> str:
        return f"{self.username} | {self.get_sex_display()}"

    def delete(self, *args, **kwargs):
        self.avatar.delete(save=False)  # Delete file directly from storage
        super().delete(*args, **kwargs)

    @property
    def username(self):
        return self.user.username

    @property
    def fullname(self) -> str | None:
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
