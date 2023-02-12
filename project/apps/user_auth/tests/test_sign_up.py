from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from ..forms import SignUpForm
from ..views import SignUpView


User = get_user_model()


class SignUpTest(TestCase):
    """User registraion view tests"""

    @classmethod
    def setUpTestData(cls):
        cls.sign_up_url = reverse("user_auth:registration")

    def test_get(self):
        """Test for view access"""
        response = self.client.get(self.sign_up_url)

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context_data["form"], SignUpForm)
        self.assertIsInstance(response.context_data["view"], SignUpView)

    def test_post_bad(self):
        payload = {
            "username": "test_user",
            "password1": "123456",
            "password2": "123456",
        }
        response = self.client.post(self.sign_up_url, data=payload)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["form"].errors)

    def test_post_ok(self):
        payload = {
            "username": "test_user",
            "password1": "qwerty432!",
            "password2": "qwerty432!",
        }
        response = self.client.post(self.sign_up_url, data=payload)

        user = User.objects.get(username=payload["username"])

        self.assertEqual(user.username, payload["username"])
        self.assertNotEqual(user.password, payload["password1"])
        self.assertEqual(response.status_code, 302)
        self.assertTrue(user.is_authenticated)
