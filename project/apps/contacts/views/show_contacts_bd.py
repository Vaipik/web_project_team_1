from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from apps.contacts.models import Contact
from utils.pagination import get_paginator
from apps.contacts.constants import CONTACTS_PER_PAGE
from apps.contacts.services import get_birthday_list


@login_required
def show_contacts_bd(request):
    """
    Shows people who have birthdays n days from now.
    """
    if request.method == "GET":

        all_contacts = Contact.objects.filter(owner=request.user, birthday__isnull=False).prefetch_related(
            "phones", "emails"
        )
        days = request.GET.get("query", "")

        if not days:
            birthday_list = all_contacts
            messages.add_message(request, messages.INFO, "Choose a period.")
        else:
            birthday_list = get_birthday_list(all_contacts, days)

        if birthday_list:
            page_obj, pages = get_paginator(request, birthday_list, CONTACTS_PER_PAGE)
            return render(
                request,
                "contacts/contact_book.html",
                {"page_obj": page_obj, "pages": pages, "search_query": days},
            )

        messages.add_message(
            request, messages.INFO, "Nobody has birthday in the given period."
        )
        return render(request, "contacts/contact_book.html")
