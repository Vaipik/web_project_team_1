from django import forms
from django.core.exceptions import ValidationError

from .models import File
from .services import determine_file_category


class FileForm(forms.ModelForm):

    class Meta:
        model = File
        fields = ["description", "file"]

    def clean_file(self):
        file = self.cleaned_data["file"]
        if determine_file_category(file.name) is None:
            raise ValidationError("Not allowed file type")
        return file
