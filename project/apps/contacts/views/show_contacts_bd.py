from django.contrib import messages
from django.shortcuts import render

from datetime import date
from dateutil.relativedelta import relativedelta

from apps.contacts.models import Contact
from utils.pagination import get_paginator


def happens_in(birthday, days):
    today = date.today()
    birthday = date(today.year, birthday.month, birthday.day)
    difference = birthday - today
    if difference.days >= 0:
        return difference.days <= relativedelta(days=days).days
    else:
        abs_difference = today + relativedelta(years=1) - difference
        return abs_difference.day <= relativedelta(days=days).days


def show_contacts_bd(request):
    if request.method == "POST":
        all_contacts = Contact.objects.filter(owner=request.user)
        days = request.POST.get("period")
        if not days:
            messages.add_message(
                request, messages.ERROR, "Please, choose a report period."
            )
            return render(request, "contacts/contact_book.html")

        contacts = []
        for cont in all_contacts:
            if happens_in(cont.birthday, int(days)):
                contacts.append(cont)

        if len(contacts) > 0:
            page_obj, pages = get_paginator(request, contacts, len(contacts))
            return render(
                request,
                "contacts/contact_book.html",
                {"contacts": contacts, "page_obj": page_obj, "pages": pages},
            )
        else:
            messages.add_message(
                request, messages.INFO, "Nobody has birthday in the given period."
            )
            return render(request, "contacts/contact_book.html")
