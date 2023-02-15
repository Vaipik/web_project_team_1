import datetime
import uuid
from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import TestCase

from apps.contacts.constants import (
    NAME_MAX_LENGTH,
    ADDRESS_MAX_LENGTH,
    URL_MAX_LENGTH,
    TYPE_MAX_LENGTH,
)
from apps.contacts.models import Contact
from utils.choices import SEX_CHOICES


def mock_uuid():
    test_uuid = 0
    return uuid.UUID(int=test_uuid)


class ContactModelTest(TestCase):
    @classmethod
    @patch("uuid.uuid4", mock_uuid)
    def setUpTestData(cls):
        user = User.objects.create_user(username="Test", password="12345")
        Contact.objects.create(
            pk=mock_uuid(),
            owner_id=user.id,
            name="Bob",
            address="Bob's street",
            birthday=datetime.date(1980, 1, 1),
            sex="m",
        )

    def test_name_label(self):
        contact = Contact.objects.get(pk=mock_uuid())
        field_label = contact._meta.get_field("name").verbose_name
        self.assertEqual(field_label, "name")

    def test_address_label(self):
        contact = Contact.objects.get(pk=mock_uuid())
        field_label = contact._meta.get_field("address").verbose_name
        self.assertEqual(field_label, "address")

    def test_birthday_label(self):
        contact = Contact.objects.get(pk=mock_uuid())
        field_label = contact._meta.get_field("birthday").verbose_name
        self.assertEqual(field_label, "birthday")

    def test_owner_label(self):
        contact = Contact.objects.get(pk=mock_uuid())
        field_label = contact._meta.get_field("owner").verbose_name
        self.assertEqual(field_label, "owner")

    def test_sex_label(self):
        contact = Contact.objects.get(pk=mock_uuid())
        field_label = contact._meta.get_field("sex").verbose_name
        self.assertEqual(field_label, "sex")

    def test_name_max_length(self):
        contact = Contact.objects.get(pk=mock_uuid())
        max_length = contact._meta.get_field("name").max_length
        self.assertEqual(max_length, NAME_MAX_LENGTH)

    def test_address_max_length(self):
        contact = Contact.objects.get(pk=mock_uuid())
        max_length = contact._meta.get_field("address").max_length
        self.assertEqual(max_length, ADDRESS_MAX_LENGTH)

    def test_sex_max_length(self):
        contact = Contact.objects.get(pk=mock_uuid())
        max_length = contact._meta.get_field("sex").max_length
        self.assertEqual(max_length, TYPE_MAX_LENGTH)

    def test_slug_max_length(self):
        contact = Contact.objects.get(pk=mock_uuid())
        max_length = contact._meta.get_field("slug").max_length
        self.assertEqual(max_length, URL_MAX_LENGTH)

    def test_sex_choices(self):
        contact = Contact.objects.get(pk=mock_uuid())
        max_length = contact._meta.get_field("sex").choices
        self.assertEqual(max_length, SEX_CHOICES)
