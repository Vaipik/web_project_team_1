from django.test import TestCase
from django.urls import reverse

from apps.user_auth.factories import UserFactory
from ..factories import FileFactory
from ..forms import FileEditForm


# EDIT_FILE_URL =


class TestFileEdit(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.file = FileFactory()
        password = "123123adad!)21212"
        user = UserFactory(password=password)
        cls.credentials = {
            "username": user.username,
            "password": password
        }

    def test_get(self):
        self.client.login(**self.credentials)
        file_owner_username = self.file.owner.username
        response = self.client.get(reverse("file_storage:edit_file", kwargs={"file_uuid": self.file.uuid}))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(file_owner_username, self.credentials["username"])  # Logged in user same as file owner
        self.assertIsInstance(response.context_data["form"], FileEditForm)
