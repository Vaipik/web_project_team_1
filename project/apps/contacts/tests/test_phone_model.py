import datetime
import uuid
from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import TestCase

from apps.contacts.constants import PHONE_MAX_LENGTH, TYPE_MAX_LENGTH
from apps.contacts.models import Contact, Phone
from utils.choices import TYPES_OF_PHONE


def mock_uuid():
    test_uuid = 0
    return uuid.UUID(int=test_uuid)


class PhoneModelTest(TestCase):
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
        phone = Phone.objects.create(
            id=1, owner=owner, phone_number="1234567890", type="p"
        )

    def test_owner_label(self):
        phone = Phone.objects.get(id=1)
        field_label = phone._meta.get_field("owner").verbose_name
        self.assertEqual(field_label, "owner")

    def test_phone_label(self):
        phone = Phone.objects.get(id=1)
        field_label = phone._meta.get_field("phone_number").verbose_name
        self.assertEqual(field_label, "phone number")

    def test_type_label(self):
        phone = Phone.objects.get(id=1)
        field_label = phone._meta.get_field("type").verbose_name
        self.assertEqual(field_label, "type")

    def test_phone_max_length(self):
        phone = Phone.objects.get(id=1)
        max_length = phone._meta.get_field("phone_number").max_length
        self.assertEqual(max_length, PHONE_MAX_LENGTH)

    def test_type_max_length(self):
        phone = Phone.objects.get(id=1)
        max_length = phone._meta.get_field("type").max_length
        self.assertEqual(max_length, TYPE_MAX_LENGTH)

    def test_type_choices(self):
        phone = Phone.objects.get(id=1)
        max_length = phone._meta.get_field("type").choices
        self.assertEqual(max_length, TYPES_OF_PHONE)
