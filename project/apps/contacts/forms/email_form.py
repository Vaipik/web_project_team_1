from django.forms import EmailField, ChoiceField
from django.core.validators import validate_email

from apps.contacts.models import Email
from apps.contacts.constants import EMAIL_MAX_LENGTH
from apps.contacts.choices import TYPES_OF_EMAIL


class EmailForm:
    email_addr = EmailField(max_length=EMAIL_MAX_LENGTH, validators=[validate_email])
    type = ChoiceField(
        choices=TYPES_OF_EMAIL, label="Work or personal", initial="", required=True
    )

    class Meta:
        model = Email
        fields = "__all__"
