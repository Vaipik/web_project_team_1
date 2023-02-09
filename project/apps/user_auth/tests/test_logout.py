from django.test import TestCase
from django.urls import reverse

from ..factories import UserFactory


class SignOutTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.logout_url = reverse("user_auth:logout")
        password = "123456789!@12aSA"
        user = UserFactory(password=password)
        cls.credentials = {
            "username": user.username,
            "password": password,
        }

    def test_get_not_auth(self):
        """User is not authenticated -> redirect to sign in url"""
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, 302)

    def test_post_not_auth(self):
        """POST with not authenticated method"""
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, 302)

    def test_get_auth(self):
        """GET not allowed -> 405"""
        self.client.login(**self.credentials)  # log in to be allower access logout page
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, 405)

    def test_post_auth(self):
        """POST request to logout for authenticated user"""
        self.client.login(**self.credentials)
        response = self.client.post(self.logout_url)

        self.assertEqual(response.status_code, 302)  # success logout and redirect to sign up
