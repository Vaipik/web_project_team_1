from django.core.exceptions import ValidationError
from django.forms import ModelForm, CharField, TextInput, Select, Textarea
from . import models
from .libs import constants


class TagForm(ModelForm):
    class Meta:
        model = models.Tag
        fields = ['name']
        widgets = {
            "name": TextInput(attrs={
                "class": "form-control mt-3",
                "placeholder": "Enter name tag"
            }),
        }
        labels = {
            "tag": "Tag name",
        }

        def clean_name(self):
            name = self.cleaned_data["name"]
            if len(name) < constants.TAG_MIN_LENGTH:
                raise ValidationError(
                    f"Minimum tag length {constants.TAG_MIN_LENGTH} characters!")
            if len(name) > constants.TAG_MAX_LENGTH:
                raise ValidationError(
                    f"Maximum tag length {constants.TAG_MAX_LENGTH} characters!")
            return name


class NoteForm(ModelForm):
    class Meta:
        model = models.Note
        fields = ['name', 'description', 'tags']
        exclude = ['tags']
        widgets = {
            "name": TextInput(attrs={
                "class": "form-control mt-3",
                "placeholder": "Enter name note"
            }),
            "description": Textarea(attrs={
                "class": "form-control mt-3 span4",
                "style": "height: 150px",
                "placeholder": "Enter note description",

            }),
            "tags": Select(attrs={
                "class": "form-control mt-3",
                "multiple": "multiple",
                "size": "10",
                "placeholder": "Select tags"
            }),
        }
        labels = {
            "note": "Note name",
            "description": "Note description",
            "tags": "",
        }

    def clean_name(self):
        name = self.cleaned_data["name"]
        if len(name) < constants.NAME_MIN_LENGTH:
            raise ValidationError(
                f"Minimum name length {constants.NAME_MIN_LENGTH} characters!")  # отримати помилку можна в через {% for error in field.errors %} {{ error }} {% endfor %}
        if len(name) > constants.NAME_MAX_LENGTH:
            raise ValidationError(
                f"Maximum name length {constants.NAME_MAX_LENGTH} characters!")
        return name

    def clean_description(self):
        description = self.cleaned_data["description"]
        if len(description) < constants.DESCRIPTION_MIN_LENGTH:
            raise ValidationError(
                f"Minimum description length {constants.DESCRIPTION_MIN_LENGTH} characters!")
        if len(description) > constants.DESCRIPTION_MAX_LENGTH:
            raise ValidationError(
                f"Maximum description length {constants.DESCRIPTION_MAX_LENGTH} characters!")
        return description
