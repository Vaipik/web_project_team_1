from django.utils import timezone
from django.forms import (
    ModelForm,
    CharField,
    EmailField,
    DateField,
    SelectDateWidget,
    ValidationError,
)
from django.contrib.postgres.forms import SimpleArrayField
from django.core.validators import validate_email, RegexValidator

from apps.contacts.models import Contact


def validate_birthdate(date):
    if date > timezone.now().date():
        raise ValidationError(f"Birth date: {date} is in future")
    return date


class ContactForm(ModelForm):
    name = CharField(
        max_length=100,
        required=True,
        validators=[
            RegexValidator(
                regex=r"^[\w ]{2,100}$",
                message="Name must be between 2 and 100 characters.",
            )
        ],
    )
    phones = SimpleArrayField(
        CharField(
            max_length=20,
            validators=[
                RegexValidator(
                    regex=r"^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$",
                    message="Invalid phone format. Try +123456789012 or 1234567890.",
                )
            ],
        )
    )
    email = EmailField(max_length=100, validators=[validate_email])
    address = CharField(max_length=200)
    birthday = DateField(
        validators=[validate_birthdate],
        widget=SelectDateWidget(years=range(2023, 1923, -1)),
    )

    class Meta:
        model = Contact
        fields = "__all__"
