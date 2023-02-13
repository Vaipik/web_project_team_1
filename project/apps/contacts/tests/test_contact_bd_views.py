import datetime
import uuid
from unittest.mock import patch

from django.test import TestCase
from django.contrib.auth.models import User

from apps.contacts.services import get_birthday_list
from apps.contacts.models import Contact

TEST_UUID = 0


def mock_uuid():
    global TEST_UUID
    TEST_UUID += 1
    return uuid.UUID(int=TEST_UUID)


class ContactBirthdayViewTest(TestCase):

    @patch("uuid.uuid4", mock_uuid)
    def setUp(self):
        self.user = User.objects.create_user(username="Test", password="12345")
        self.people = [
            Contact.objects.create(pk=mock_uuid(), owner_id=self.user.id, name="Bob", sex="m",
                                   birthday=datetime.date(1987, 2, 1)),
            Contact.objects.create(pk=mock_uuid(), owner_id=self.user.id, name="Vasya", sex="m",
                                   birthday=datetime.date(1997, 3, 1)),
            Contact.objects.create(pk=mock_uuid(), owner_id=self.user.id, name="Kate", sex="f",
                                   birthday=datetime.date(1987, 2, 15)),
            Contact.objects.create(pk=mock_uuid(), owner_id=self.user.id, name="Mary", sex="f",
                                   birthday=datetime.date(1997, 3, 9)),
            Contact.objects.create(pk=mock_uuid(), owner_id=self.user.id, name="Trevor", sex="m",
                                   birthday=datetime.date(2000, 2, 20)),
            Contact.objects.create(pk=mock_uuid(), owner_id=self.user.id, name="Dany", sex="m",
                                   birthday=datetime.date(2001, 3, 15)),
            Contact.objects.create(pk=mock_uuid(), owner_id=self.user.id, name="Sunny", sex="m",
                                   birthday=datetime.date(1977, 4, 3)),
        ]

    def test_birthday_in_a_week(self):
        period = 7
        result = get_birthday_list(self.people, period)
        contacts_names = [contact.name for contact in result]
        self.assertEqual(len(result), 2)
        self.assertTrue("Kate" in contacts_names)
        self.assertTrue("Trevor" in contacts_names)

    def test_birthday_in_a_month(self):
        period = 31
        result = get_birthday_list(self.people, period)
        contacts_names = [contact.name for contact in result]
        self.assertEqual(len(result), 5)
        self.assertTrue("Kate" in contacts_names)
        self.assertTrue("Trevor" in contacts_names)
        self.assertTrue("Vasya" in contacts_names)
        self.assertTrue("Mary" in contacts_names)
        self.assertTrue("Dany" in contacts_names)

    def test_birthday_in_a_year(self):
        period = 365
        result = get_birthday_list(self.people, period)
        contacts_names = [contact.name for contact in result]
        self.assertEqual(len(result), 7)
        self.assertTrue("Kate" in contacts_names)
        self.assertTrue("Trevor" in contacts_names)
        self.assertTrue("Vasya" in contacts_names)
        self.assertTrue("Mary" in contacts_names)
        self.assertTrue("Bob" in contacts_names)
        self.assertTrue("Dany" in contacts_names)
        self.assertTrue("Sunny" in contacts_names)
