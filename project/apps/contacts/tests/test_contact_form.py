import datetime

from django.test import TestCase

from apps.contacts.forms import ContactForm
from apps.contacts.constants import NAME_MAX_LENGTH, ADDRESS_MAX_LENGTH
from utils.choices import SEX_CHOICES


class ContactFormTest(TestCase):
    def test_name_field_label(self):
        form = ContactForm()
        self.assertTrue(
            form.fields["name"].label is None or form.fields["name"].label == "name"
        )

    def test_address_field_label(self):
        form = ContactForm()
        self.assertTrue(
            form.fields["address"].label is None
            or form.fields["address"].label == "address"
        )

    def test_birthday_field_label(self):
        form = ContactForm()
        self.assertTrue(
            form.fields["birthday"].label is None
            or form.fields["birthday"].label == "birthday"
        )

    def test_sex_field_label(self):
        form = ContactForm()
        self.assertTrue(
            form.fields["sex"].label is None or form.fields["sex"].label == "Sex"
        )

    def test_name_max_length(self):
        form = ContactForm()
        self.assertTrue(form.fields["name"].max_length == NAME_MAX_LENGTH)

    def test_address_max_length(self):
        form = ContactForm()
        self.assertTrue(form.fields["address"].max_length == ADDRESS_MAX_LENGTH)

    def test_sex_choices(self):
        form = ContactForm()
        self.assertTrue(form.fields["sex"].choices == list(SEX_CHOICES))

    def test_name_validator(self):
        valid_form = ContactForm(data={"name": "Bob", "sex": "m"})
        self.assertTrue(valid_form.is_valid())
        invalid_form = ContactForm(data={"name": "B", "sex": "m"})
        self.assertFalse(invalid_form.is_valid())
        self.assertEqual(
            invalid_form.errors["name"][0], "Name must be between 2 and 100 characters."
        )

    def test_birthday_validator(self):
        valid_birthday = datetime.date(1980, 1, 1)
        invalid_birthday = datetime.date(2024, 1, 1)
        valid_form = ContactForm(
            data={"name": "Bob", "birthday": valid_birthday, "sex": "m"}
        )
        self.assertTrue(valid_form.is_valid())
        invalid_form = ContactForm(
            data={"name": "Bob", "birthday": invalid_birthday, "sex": "m"}
        )
        self.assertFalse(invalid_form.is_valid())
        self.assertEqual(
            invalid_form.errors["birthday"][0],
            f"Birth date: {invalid_birthday} is in future",
        )

    def test_birthday_widget_years(self):
        form = ContactForm()
        self.assertTrue(form.fields["birthday"].widget.years == range(2023, 1923, -1))
