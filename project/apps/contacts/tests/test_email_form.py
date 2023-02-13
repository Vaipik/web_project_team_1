from django.test import TestCase

from apps.contacts.forms import EmailForm
from apps.contacts.constants import EMAIL_MAX_LENGTH
from utils.choices import TYPES_OF_EMAIL


class TestEmailForm(TestCase):
    def test_email_field_label(self):
        form = EmailForm()
        self.assertTrue(
            form.fields["email_addr"].label is None
            or form.fields["email_addr"].label == "email_addr"
        )

    def test_type_label(self):
        form = EmailForm()
        self.assertTrue(
            form.fields["type"].label is None
            or form.fields["type"].label == "Work or personal"
        )

    def test_email_max_length(self):
        form = EmailForm()
        self.assertTrue(form.fields["email_addr"].max_length == EMAIL_MAX_LENGTH)

    def test_type_choices(self):
        form = EmailForm()
        self.assertTrue(form.fields["type"].choices == list(TYPES_OF_EMAIL))
