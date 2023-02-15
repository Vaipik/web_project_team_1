import uuid
from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.test import Client

from apps.contacts.models import Contact
from apps.contacts.constants import CONTACTS_PER_PAGE


TEST_UUID = 0


def mock_uuid():
    global TEST_UUID
    TEST_UUID += 1
    return uuid.UUID(int=TEST_UUID)


class ContactListViewTest(TestCase):
    @patch("uuid.uuid4", mock_uuid)
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="Test", password="12345")
        self.client.login(username="Test", password="12345")
        self.number_of_contacts = 9

        for contact_id in range(self.number_of_contacts):
            Contact.objects.create(
                pk=mock_uuid(),
                owner_id=self.user.id,
                name=f"Bob {contact_id}",
                sex="m",
            )

    def test_view_url(self):
        response = self.client.get("/contacts/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_by_name(self):
        response = self.client.get(reverse("contacts:contacts"))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse("contacts:contacts"))
        self.assertTemplateUsed(response, "contacts/contact_book.html")

    def test_pagination_exists(self):
        response = self.client.get(reverse("contacts:contacts"))
        self.assertTrue("page_obj" in response.context)
        self.assertTrue(len(response.context["page_obj"]) == CONTACTS_PER_PAGE)
        self.assertTrue("pages" in response.context)

    def test_second_page_length(self):
        response = self.client.get(reverse("contacts:contacts") + "?page=2")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("page_obj" in response.context)
        self.assertTrue("pages" in response.context)
        self.assertEqual(
            len(response.context["page_obj"]),
            self.number_of_contacts - CONTACTS_PER_PAGE,
        )
