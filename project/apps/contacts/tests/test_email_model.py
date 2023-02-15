import datetime
import uuid
from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import TestCase

from apps.contacts.constants import EMAIL_MAX_LENGTH, TYPE_MAX_LENGTH
from apps.contacts.models import Contact, Email
from utils.choices import TYPES_OF_EMAIL


def mock_uuid():
    test_uuid = 0
    return uuid.UUID(int=test_uuid)


class EmailModelTest(TestCase):
    @classmethod
    @patch("uuid.uuid4", mock_uuid)
    def setUpTestData(cls):
        user = User.objects.create_user(username="Test", password="12345")
        owner = Contact.objects.create(
            pk=mock_uuid(),
            owner_id=user.id,
            name="Bob",
            address="Bob's street",
            birthday=datetime.date(1980, 1, 1),
            sex="m",
        )
        email = Email.objects.create(
            id=1, owner=owner, email_addr="bob@gmail.com", type="w"
        )

    def test_owner_label(self):
        email = Email.objects.get(id=1)
        field_label = email._meta.get_field("owner").verbose_name
        self.assertEqual(field_label, "owner")

    def test_email_label(self):
        email = Email.objects.get(id=1)
        field_label = email._meta.get_field("email_addr").verbose_name
        self.assertEqual(field_label, "email addr")

    def test_type_label(self):
        email = Email.objects.get(id=1)
        field_label = email._meta.get_field("type").verbose_name
        self.assertEqual(field_label, "type")

    def test_email_max_length(self):
        email = Email.objects.get(id=1)
        max_length = email._meta.get_field("email_addr").max_length
        self.assertEqual(max_length, EMAIL_MAX_LENGTH)

    def test_type_max_length(self):
        email = Email.objects.get(id=1)
        max_length = email._meta.get_field("type").max_length
        self.assertEqual(max_length, TYPE_MAX_LENGTH)

    def test_type_choices(self):
        email = Email.objects.get(id=1)
        max_length = email._meta.get_field("type").choices
        self.assertEqual(max_length, TYPES_OF_EMAIL)
