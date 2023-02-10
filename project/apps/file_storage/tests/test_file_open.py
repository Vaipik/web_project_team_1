from django.test import TestCase, override_settings
from django.urls import reverse

from apps.user_auth.factories import UserFactory
from ..factories import FileFactory
from ..views import FileDetailView
from .dropbox_env_settings import dropbox_env


@override_settings(**dropbox_env)
class TestFileOpen(TestCase):

    @classmethod
    def setUpTestData(cls):
        """Setting up test data"""
        cls.file = FileFactory()
        password = "123123adad!)21212"  # user password
        user = UserFactory(password=password)
        cls.credentials = {
            "username": user.username,
            "password": password
        }
        cls.file_open_url = reverse("file_storage:show_file", kwargs={"file_uuid": cls.file.uuid})  # testing url

    def test_get_unauthorized(self):
        """If unauthorized -> redirect to sign up page"""
        response = self.client.get(self.file_open_url)

        self.assertEqual(response.status_code, 302)  # redirect because user not authorized

    def test_get_authorized(self):
        """GET request for authorized user"""
        self.client.login(**self.credentials)
        response = self.client.get(self.file_open_url)

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context_data["view"], FileDetailView)

    def test_post_unauthorized(self):
        """POST request for unauthorized user -> redirect to sign up"""
        response = self.client.post(self.file_open_url)
        self.assertEqual(response.status_code, 302)

    def test_post_authorized(self):
        """POST request for authorized user -> 405 not allowed"""
        self.client.login(**self.credentials)
        response = self.client.post(self.file_open_url)
        self.assertEqual(response.status_code, 405)  # Not allowed
