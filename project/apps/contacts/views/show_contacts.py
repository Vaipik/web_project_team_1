from django.shortcuts import render
from django.core.exceptions import PermissionDenied

from apps.contacts.models import Contact, Email, Phone


def show_contacts(request):
    if request.user.is_authenticated:
        contacts = Contact.objects.filter(user=request.user).all()
        return render(request, "contacts/contact_book.html", {"contacts": contacts})
    else:
        raise PermissionDenied
