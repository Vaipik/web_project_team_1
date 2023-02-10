from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from ..factories import UserFactory


User = get_user_model()


class SignInTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.sign_in_url = reverse("user_auth:login")
        password = "123123ASAS!!@(SA"
        user = UserFactory(password=password)
        credentials = {
            "username": user.username,
        }
        cls.valid_credentials = dict(**credentials, password=password)
        cls.invalid_credentials = dict(**credentials, password="123123123asdasdasd")

    def test_get(self):
        """GET method not allowed"""
        response = self.client.get(self.sign_in_url)

        self.assertEqual(response.status_code, 405)

    def test_post_no_credentials(self):
        """POST with empty credentials"""
        response = self.client.post(self.sign_in_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], 400)

    def test_post_bad_credentials(self):
        """POST with wrong password"""
        response = self.client.post(self.sign_in_url, data=self.invalid_credentials)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], 400)

    def test_post_success(self):
        """POST with correct credentials"""

        response = self.client.post(self.sign_in_url, data=self.valid_credentials)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], 200)
