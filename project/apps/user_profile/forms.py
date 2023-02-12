from django import forms

from .models import Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ("user",)
        widgets = {
            "first_name": forms.TextInput(attrs={
                "class": "form-control mt-2 fw-light",
                "placeholder": "Enter you first name"
            }),
            "last_name": forms.TextInput(attrs={
                "class": "form-control mt-2 fw-light",
                "placeholder": "Enter you last name"
            }),
            "phone": forms.TextInput(attrs={
                "class": "form-control mt-2 fw-light",
                "placeholder": "Enter you phone number",
            }),
            "email": forms.EmailInput(attrs={
                "class": "form-control mt-2 fw-light",
                "placeholder": "Enter you email address",
            }),
            "sex": forms.Select(attrs={
                "class": "form-select mt-2 fw-light",
                "placeholder": "Select your gender",
            }),
            "avatar": forms.FileInput(attrs={
                "class": "form-control mt-2 fw-light",
                "placeholder": "You avatar profile"
            })
        }
        labels = {
            "first_name": "First name",
            "last_name": "Last name",
            "sex": "Gender",
        }
