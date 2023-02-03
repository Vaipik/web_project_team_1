from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from ..factories import UserFactory


User = get_user_model()


class SignOutTest(TestCase):

    def test_get(self):
        response = self.client.get(reverse("user_auth:login"))

        self.assertEqual(response.status_code, 405)

    def test_post_no_credentials(self):
        response = self.client.post(reverse("user_auth:login"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], 400)

    def test_post_bad_credentials(self):

        user = UserFactory()
        payload = {
            "username": user.username,
            "password": "1233123213"
        }
        response = self.client.post(reverse("user_auth:login"), data=payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], 400)

    def test_post_success(self):

        password = "123123ASAS!!@(SA"
        user = UserFactory(password=password)
        payload = {
            "username": user.username,
            "password": password,
        }
        response = self.client.post(reverse("user_auth:login"), data=payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], 200)
