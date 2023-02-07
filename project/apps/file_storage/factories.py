import random
from string import ascii_letters

import factory.fuzzy

from apps.user_auth.factories import UserFactory

from utils.file_categories import Categories
from apps.file_storage.models import File


def _get_random_extension() -> str:
    category = random.choice(list(Categories)).value
    extension = f".{random.choice(category)}"
    return extension


def random_file() -> str:
    return ''.join(random.sample(ascii_letters, k=10)) + _get_random_extension()


class FileFactory(factory.django.DjangoModelFactory):

    description = factory.fuzzy.FuzzyText()
    file = factory.django.FileField(
        filename=random_file()
    )

    owner = factory.SubFactory(UserFactory)

    class Meta:
        model = File

