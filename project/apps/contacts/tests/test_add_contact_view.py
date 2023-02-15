import uuid

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.test import Client


TEST_UUID = 0


def mock_uuid():
    global TEST_UUID
    TEST_UUID += 1
    return uuid.UUID(int=TEST_UUID)


class ContactAddViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="Test", password="12345")
        self.login = self.client.login(username="Test", password="12345")

    def test_view_url(self):
        response = self.client.get("/contacts/add_contact/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_by_name(self):
        response = self.client.get(reverse("contacts:add_contact"))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse("contacts:add_contact"))
        self.assertTemplateUsed(response, "contacts/contact_add.html")

    def test_post_success(self):
        response = self.client.post("/contacts/add_contact/", data={"cont_form-name": "Bob",
                                                                    "cont_form-sex": "m",
                                                                    "email_form-TOTAL_FORMS": 2,
                                                                    "email_form-INITIAL_FORMS": 0,
                                                                    "email_form-0-email_addr": "bob@gmail.com",
                                                                    "email_form-0-type": "w",
                                                                    "email_form-1-DELETE": "on",
                                                                    "phone_form-TOTAL_FORMS": 2,
                                                                    "phone_form-INITIAL_FORMS": 0,
                                                                    "phone_form-0-phone_number": "0980980987",
                                                                    "phone_form-0-type": "w",
                                                                    "phone_form-1-DELETE": "on"}, follow=True)

        self.assertRedirects(response, '/contacts/', status_code=302, fetch_redirect_response=True)
        self.assertContains(response, "A new contact added successfully!")

    def test_post_error(self):
        response = self.client.post("/contacts/add_contact/", data={"cont_form-name": "Bob",
                                                                    "email_form-TOTAL_FORMS": 2,
                                                                    "email_form-INITIAL_FORMS": 0,
                                                                    "email_form-0-email_addr": "bob@gmail.com",
                                                                    "email_form-0-type": "w",
                                                                    "email_form-1-DELETE": "on",
                                                                    "phone_form-TOTAL_FORMS": 2,
                                                                    "phone_form-INITIAL_FORMS": 0,
                                                                    "phone_form-0-phone_number": "0980980987",
                                                                    "phone_form-0-type": "w",
                                                                    "phone_form-1-DELETE": "on"}, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This field is required")
