from uuid import uuid4

from autoslug import AutoSlugField
from django.db import models
from django.contrib.auth.models import User
from PIL import Image

from .libs import constants
from utils.file_categories import _get_folder_name


class Profile(models.Model):
    uuid = models.UUIDField(
        default=uuid4,
        primary_key=True,
        editable=False
    )
    first_name = models.CharField(
        max_length=constants.FIRSTNAME_MAX_LENGTH,
        verbose_name="First name"
    )
    last_name = models.CharField(
        max_length=constants.LASTNAME_MAX_LENGTH,
        verbose_name="Last name"
    )
    phone = models.CharField(max_length=constants.PHONE_MAX_LENGTH)
    email = models.CharField(max_length=constants.EMAIL_MAX_LENGTH)
    slug = AutoSlugField(
        populate_from="user",
        unique=True,
        max_length=constants.PROFILE_MAX_URL
    )
    sex = models.CharField(
        max_length=1,
        choices=
    )
    avatar = models.ImageField(upload_to=_get_folder_name)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # resizing images
    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.avatar.path)

        if img.height > 100 or img.width > 100:
            new_img = (100, 100)
            img.thumbnail(new_img)
            img.save(self.avatar.path)

    @property
    def username(self):
        return self.user.username

    @property
    def fullanme(self):
        return self.first_name + self.last_name
