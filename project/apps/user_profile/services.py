from pathlib import Path

from django.contrib.auth import get_user_model

from apps.contacts.models import Contact
from apps.notes.models import Note
from apps.file_storage.models import File
from .models import Profile


User = get_user_model()


def get_last_five_contacts(user: User):
    return Contact.objects.filter(owner=user)[:5]


def get_last_five_files(user: User):
    return File.objects.select_related("category").filter(owner=user)[:5]


def get_last_five_notes(user: User):
    return Note.objects.filter(user=user)[:5]


def count_user_contacts(user: User):
    return Contact.objects.filter(owner=user).count()


def count_user_files(user: User):
    return File.objects.filter(owner=user).count()


def count_user_notes(user: User):
    return Note.objects.filter(user=user).count()


def get_profile_context(user: User):
    """Accumulating context for user profile"""
    last_contacts = get_last_five_contacts(user)
    last_files = get_last_five_files(user)
    last_notes = get_last_five_notes(user)
    contacts_amount = count_user_contacts(user)
    files_amount = count_user_files(user)
    notes_amount = count_user_notes(user)
    profile = Profile.objects.get(user=user)
    return {
        "contacts": last_contacts,
        "files": last_files,
        "notes": last_notes,
        "contacts_amount": contacts_amount,
        "files_amount": files_amount,
        "notes_amount": notes_amount,
        "profile": profile,
    }
