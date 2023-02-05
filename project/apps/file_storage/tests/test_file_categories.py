from django.test import TestCase

from ..services import determine_file_category, get_file_category
from ..models import FileCategory
from ..factories import random_file


class CategoryTest(TestCase):

    def test_determine_file_category_ok(self):
        "File with valid extension"
        for _ in range(10):
            file = random_file()
            result = determine_file_category(file)
            self.assertTrue(result)

    def test_determine_file_category_None(self):
        """File is invalid"""
        for _ in range(10):
            file = random_file()[:-2]  # making file extension invalid
            result = determine_file_category(file)
            self.assertIsNone(result)

    def test_get_file_category(self):
        for _ in range(10):
            file = random_file()
            result = get_file_category(file)
            self.assertIsInstance(result, FileCategory)

