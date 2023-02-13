import uuid
from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.test import Client

from apps.contacts.models import Contact


TEST_UUID = 0


def mock_uuid():
    global TEST_UUID
    TEST_UUID += 1
    return uuid.UUID(int=TEST_UUID)


class ContactDeleteViewTest(TestCase):
    @patch("uuid.uuid4", mock_uuid)
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="Test", password="12345")
        self.client.login(username="Test", password="12345")
        self.contact = Contact.objects.create(pk=mock_uuid(), owner_id=self.user.id, name="Bob", sex="m")

    def test_deletion(self):
        response = self.client.post(reverse("contacts:delete_contact", args=(self.contact.pk,)), follow=True)
        self.assertContains(response, "Deleted successfully!")
        self.assertEqual(response.status_code, 200)
