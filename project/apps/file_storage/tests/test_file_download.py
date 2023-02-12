from django.test import TestCase, override_settings
from django.urls import reverse

from apps.user_auth.factories import UserFactory
from ..factories import FileFactory

from .dropbox_env_settings import dropbox_env


@override_settings(**dropbox_env)
class TestFileDownload(TestCase):

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
        cls.file_open_url = reverse("file_storage:show_file", kwargs={"file_uuid": cls.file.uuid})

    def test_get(self):
        """NEED TO BE FIXED. WILL ALWAYS FAILING UNTIL TESTED IN REAL CLOUD"""
        self.client.login(**self.credentials)
        response = self.client.get(self.file_open_url)
        file_download_url = response.context_data["file"].file.url
        self.assertTrue(file_download_url)
