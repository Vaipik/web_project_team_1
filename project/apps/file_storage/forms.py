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
                "class": "form-control mt-3",
                "placeholder": "Enter file description"
            }),
            "file": forms.FileInput(attrs={
                "class": "form-control form-control-lg mt-3",
            })
        }
        labels = {
            "description": "Enter the file description",
        }

    def clean_file(self):
        file = self.cleaned_data["file"]
        if determine_file_category(file.name) is None:
            raise ValidationError("Not allowed file type")
        return file


class EditFileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ["description"]
        widgets = {
            "description": forms.TextInput(attrs={
                "class": "form-control mt-3",
                "placeholder": "Edit file description"
            }),
        }
        labels = {
            "description": "Edit the file description",
        }
