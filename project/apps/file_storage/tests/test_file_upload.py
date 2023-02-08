from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse, resolve
from dotenv import dotenv_values

from apps.user_auth.factories import UserFactory
from ..views import UploadFileView
from ..forms import FileUploadForm

from ..factories import random_file


UPLOAD_URL = reverse("file_storage:upload_file")


class TestFileUpload(TestCase):

    @classmethod
    def setUpTestData(cls):
        password = "123123adad!)21212"
        user = UserFactory(password=password)
        invalid_filename = random_file()[:-2]
        invalid_file = SimpleUploadedFile(invalid_filename, b"123213123123")
        valid_filename = random_file()
        valid_file = SimpleUploadedFile(valid_filename, b"123213123123")
        cls.credentials = {
            "username": user.username,
            "password": password
        }
        payload = {
            "description": "File description",
        }
        cls.valid_payload = dict(**payload, file=valid_file)
        cls.invalid_payload = dict(**payload, file=invalid_file)

    def test_get_unauthorized(self):
        response = self.client.get(UPLOAD_URL)
        self.assertEqual(response.status_code, 302)

    def test_get_authorized(self):

        self.client.login(**self.credentials)
        response = self.client.get(UPLOAD_URL)

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context_data["form"],FileUploadForm)
        self.assertIsInstance(response.context_data["view"], UploadFileView)

    def test_post_invalid(self):
        self.client.login(**self.credentials)
        response = self.client.post(UPLOAD_URL, data=self.invalid_payload)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context_data["form"].errors)

    def test_post_valid(self):
        self.client.login(**self.credentials)
        response = self.client.post(UPLOAD_URL, data=self.valid_payload)

        self.assertEqual(response.status_code, 302)  # redirect to /files/
        self.assertEqual(response.url, "/files/")
