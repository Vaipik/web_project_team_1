from django.test import TestCase
from django.urls import reverse

from ..factories import UserFactory


class SignOutTest(TestCase):

    def test_get_not_auth(self):
        """User is not authenticated -> redirect to sign in url"""
        response = self.client.get(reverse("user_auth:logout"))
        self.assertEqual(response.status_code, 302)

    def test_post_not_auth(self):
        """POST with not authenticated method"""
        response = self.client.post(reverse("user_auth:logout"))
        self.assertEqual(response.status_code, 302)

    def test_get_auth(self):
        """GET not allowed -> 405"""
        password = "123456789!@12aSA"
        user = UserFactory(password=password)
        payload = {
            "username": user.username,
            "password": password,
        }
        self.client.login(**payload)
        response = self.client.get(reverse("user_auth:logout"))

        self.assertEqual(response.status_code, 405)

    def test_post_auth(self):
        """POST request to logout for authenticated user"""
        password = "123456789!@12aSA"
        user = UserFactory(password=password)
        payload = {
            "username": user.username,
            "password": password,
        }
        self.client.login(**payload)
        response = self.client.post(reverse("user_auth:logout"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], 302)
        self.assertEqual(response.json()["url"], reverse("user_auth:registration"))
