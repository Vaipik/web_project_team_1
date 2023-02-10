from uuid import uuid4

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import QuerySet
from django.test import TestCase

from .. import services
from ..factories import FileFactory
from ..models import File


class TestFileServices(TestCase):

    @classmethod
    def setUpTestData(cls):
        """Setting up test data"""
        cls.file = FileFactory()
        cls.user = cls.file.owner
        cls.category = cls.file.category

    def test_get_user_files(self):
        """Getting user files"""
        result = services.get_user_files(self.user)

        self.assertIsInstance(result, QuerySet)  # check return
        self.assertIsInstance(result.first(), File)  # check items

    def test_get_file(self):
        """Getting single file"""
        result = services.get_file(self.file.uuid)
        self.assertIsInstance(result, File)  # check return instance
        self.assertEqual(self.file, result)  # check if files are equal

        try:
            services.get_file(uuid4())  # try to get file which does not exist
        except Exception as e:
            self.assertIsInstance(e, ObjectDoesNotExist)  # Catching error if file does not exist

    def test_get_user_category_files(self):
        """Getting user files by using category_url"""
        result = services.get_user_category_files(self.user, self.category.slug)
        self.assertIsInstance(result, QuerySet)  # check return instance
        self.assertIsInstance(result.first(), File)  # check return item
        self.assertEqual(result.first(), self.file)  # check if files are equal
