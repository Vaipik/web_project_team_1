from django.forms import EmailField, ChoiceField, ModelForm, EmailInput, Select
from django.core.validators import validate_email

from apps.contacts.models import Email
from apps.contacts.constants import EMAIL_MAX_LENGTH
from utils.choices import TYPES_OF_EMAIL


class EmailForm(ModelForm):
    """
    Form for person's email.
    """

    email_addr = EmailField(
        max_length=EMAIL_MAX_LENGTH,
        validators=[validate_email],
        widget=EmailInput(
            attrs={"class": "form-control", "placeholder": "abc@abc.com"}
        ),
    )
    type = ChoiceField(
        choices=TYPES_OF_EMAIL,
        label="Work or personal",
        initial="",
        required=True,
        widget=Select(attrs={"class": "form-select"}),
    )

    class Meta:
        model = Email
        exclude = (
            "owner",
            "id",
        )
