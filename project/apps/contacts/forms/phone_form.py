from django.forms import CharField, ChoiceField, ModelForm, TextInput, Select
from django.core.validators import RegexValidator

from apps.contacts.models import Phone
from apps.contacts.constants import PHONE_MAX_LENGTH
from utils.choices import TYPES_OF_PHONE


class PhoneForm(ModelForm):
    """
    Form for person's phone.
    """

    phone_number = CharField(
        max_length=PHONE_MAX_LENGTH,
        validators=[
            RegexValidator(
                regex=r"^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$",
                message="Invalid phone format. Try +123456789012 or 1234567890.",
            )
        ],
        widget=TextInput(attrs={"class": "form-control"}),
    )
    type = ChoiceField(
        choices=TYPES_OF_PHONE,
        label="Work or personal",
        initial="",
        required=True,
        widget=Select(attrs={"class": "form-select"}),
    )

    class Meta:
        model = Phone
        exclude = (
            "owner",
            "id",
        )
