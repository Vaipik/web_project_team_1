from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse, resolve
from dotenv import dotenv_values

from apps.user_auth.factories import UserFactory
from ..views import UploadFileView
from ..forms import FileUploadForm

from ..models import File
from ..factories import random_file

UPLOAD_URL = reverse("file_storage:upload_file")


class TestFileUpload(TestCase):

    @classmethod
    def setUpTestData(cls):
        """Setting up test data"""
        password = "123123adad!)21212"  # user passowrd
        user = UserFactory(password=password)
        invalid_filename = random_file()[:-2]  # creating filename with invalid extension
        invalid_file = SimpleUploadedFile(invalid_filename, b"123213123123")  # creating invalid file object
        valid_filename = random_file()  # creating filename name with valid extension
        valid_file = SimpleUploadedFile(valid_filename, b"123213123123")  # creating valid file object
        # data for login
        cls.credentials = {
            "username": user.username,
            "password": password
        }
        # data for POST form
        payload = {
            "description": "File description",
        }
        cls.valid_payload = dict(**payload, file=valid_file)  # updating data payload for invalid file
        cls.invalid_payload = dict(**payload, file=invalid_file)  # updating data payload for valid file

    def test_get_unauthorized(self):
        """Unauthorized file upload -> 302 sign up page"""
        response = self.client.get(UPLOAD_URL)
        self.assertEqual(response.status_code, 302)

    def test_get_authorized(self):
        """GET request authorized user"""
        self.client.login(**self.credentials)
        response = self.client.get(UPLOAD_URL)

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context_data["form"], FileUploadForm)  # Form for file uploading
        self.assertIsInstance(response.context_data["view"], UploadFileView)

    def test_post_invalid(self):
        """POST request for invalid file type"""
        self.client.login(**self.credentials)
        response = self.client.post(UPLOAD_URL, data=self.invalid_payload)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context_data["form"].errors)  # checks that form returns with validation errors

    def test_post_valid(self):
        """POST request for valid file type"""
        self.client.login(**self.credentials)
        response = self.client.post(UPLOAD_URL, data=self.valid_payload)

        self.assertEqual(response.status_code, 302)  # redirect after success file upload
        self.assertEqual(response.url, reverse("file_storage:file_list"))  # checks redirect url
