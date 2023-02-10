from django.utils import timezone
from django.forms import (
    ModelForm,
    CharField,
    DateField,
    ChoiceField,
    SelectDateWidget,
    ValidationError,
)
from django.core.validators import RegexValidator

from apps.contacts.models import Contact
from apps.contacts.constants import (
    NAME_MAX_LENGTH,
    ADDRESS_MAX_LENGTH,
)
from apps.contacts.choices import SEX_CHOICES


def validate_birthdate(date):
    if date > timezone.now().date():
        raise ValidationError(f"Birth date: {date} is in future")
    return date


class ContactForm(ModelForm):
    """
    Form for information about a person.
    """
    name = CharField(
        max_length=NAME_MAX_LENGTH,
        required=True,
        validators=[
            RegexValidator(
                regex=r"^[\w .]{2,100}$",
                message="Name must be between 2 and 100 characters. And contain only letters.",
            )
        ],
    )
    address = CharField(max_length=ADDRESS_MAX_LENGTH)
    birthday = DateField(
        validators=[validate_birthdate],
        widget=SelectDateWidget(years=range(2023, 1923, -1)),
    )
    sex = ChoiceField(choices=SEX_CHOICES, label="Sex", initial="")

    class Meta:
        model = Contact
        exclude = ("owner",)
