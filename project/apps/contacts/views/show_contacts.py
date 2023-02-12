from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from apps.contacts.models import Contact
from utils.pagination import get_paginator
from apps.contacts.constants import CONTACTS_PER_PAGE


@login_required
def show_contacts(request):
    """
    Shows all contacts.
    """
    contacts = Contact.objects.filter(owner=request.user).prefetch_related(
        "phones", "emails"
    )
    if contacts:
        page_obj, pages = get_paginator(request, contacts, CONTACTS_PER_PAGE)
        return render(
            request,
            "contacts/contact_book.html",
            {"contacts": contacts, "page_obj": page_obj, "pages": pages},
        )
    else:
        return render(request, "contacts/contact_book.html")
