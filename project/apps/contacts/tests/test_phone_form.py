from django.test import TestCase

from apps.contacts.forms import PhoneForm
from apps.contacts.constants import PHONE_MAX_LENGTH
from utils.choices import TYPES_OF_PHONE


class TestPhoneForm(TestCase):
    def test_phone_field_label(self):
        form = PhoneForm()
        self.assertTrue(
            form.fields["phone_number"].label is None
            or form.fields["phone_number"].label == "phone_number"
        )

    def test_type_label(self):
        form = PhoneForm()
        self.assertTrue(
            form.fields["type"].label is None
            or form.fields["type"].label == "Work or personal"
        )

    def test_phone_max_length(self):
        form = PhoneForm()
        self.assertTrue(form.fields["phone_number"].max_length == PHONE_MAX_LENGTH)

    def test_type_choices(self):
        form = PhoneForm()
        self.assertTrue(form.fields["type"].choices == list(TYPES_OF_PHONE))

    def test_phone_validator(self):
        valid_phone = "0980980998"
        invalid_phone = "123"
        valid_form = PhoneForm(data={"phone_number": valid_phone, "type": "p"})
        self.assertTrue(valid_form.is_valid())
        invalid_form = PhoneForm(data={"phone_number": invalid_phone, "type": "p"})
        self.assertFalse(invalid_form.is_valid())
        self.assertEqual(
            invalid_form.errors["phone_number"][0],
            "Invalid phone format. Try +123456789012 or 1234567890.",
        )
