from django.test import TestCase
from django.urls import reverse

from apps.user_auth.factories import UserFactory
from ..factories import FileFactory
from ..forms import FileEditForm


class TestFileEdit(TestCase):

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
        cls.edit_url = reverse("file_storage:edit_file", kwargs={"file_uuid": cls.file.uuid})  # testing url

    def test_get_unauthorized(self):
        """GET request -> 302 sign up page"""
        response = self.client.get(self.edit_url)
        self.assertEqual(response.status_code, 302)

    def test_get_authorized(self):
        """GET request authroized -> checking form"""
        self.client.login(**self.credentials)
        file_owner_username = self.file.owner.username
        response = self.client.get(self.edit_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(file_owner_username, self.credentials["username"])  # Logged in user same as file owner
        self.assertIsInstance(response.context_data["form"], FileEditForm)

    def test_post(self):
        """
        POST request authorized user.
        Unauthorized access does not testing because
        user must be able to access this page only after file detail view
        """
        self.client.login(**self.credentials)
        form = self.client.get(self.edit_url).context_data["form"]  # get form data
        form_data = form.initial

        self.assertEqual(len(form_data), 1)  # Only one field to be edited
        edited_description = "Edited_data_description"
        form_data["description"] = edited_description  # edit form data
        self.client.post(self.edit_url, data=form_data)  # post edited form data
        response = self.client.get(self.edit_url)  # get updated form data

        self.assertEqual(response.status_code, 200)
        # Edited description match to POST form data -> form was updated
        self.assertEqual(response.context_data["form"].initial["description"], edited_description)

    def tearDown(self) -> None:
        """Delete created file"""
        self.file.delete()
