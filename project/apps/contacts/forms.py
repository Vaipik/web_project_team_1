from django.forms import ModelForm, CharField, EmailField, DateField, SelectDateWidget

from models import Contact

def validate_name(name):
    pass


def validate_birthdate(date):
    pass


class ContactForm(ModelForm):
    name = CharField(max_length=100, required=True, validators=[validate_name])
    phones = CharField()
    email = EmailField(max_length=100)
    address = CharField(max_length=200)
    birthday = DateField(validators=[validate_birthdate], widget=SelectDateWidget)

    class Meta:
        model = Contact
