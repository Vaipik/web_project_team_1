from django import forms
from django.core.exceptions import ValidationError

from .models import File
from .services import determine_file_category


class FileForm(forms.ModelForm):

    class Meta:
        model = File
        fields = ["description", "file"]
        widgets = {
            "description": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter file description"
            }),
            "file": forms.FileInput(attrs={
                "class": "form-control",
                "placeholder": "Choose the file to be uploaded"
            })
        }
        labels = {
            "description": "Enter the file description",
            "file": "Choose the file to be uploaded"
        }

    def clean_file(self):
        file = self.cleaned_data["file"]
        if determine_file_category(file.name) is None:
            raise ValidationError("Not allowed file type")
        return file
