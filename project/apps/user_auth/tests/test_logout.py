from django.test import TestCase
from django.urls import reverse


class SignOutTest(TestCase):

    def test_get(self):
        response = self.client.get(reverse("user_auth:logout"))

        self.assertEqual(response.status_code, 302)
