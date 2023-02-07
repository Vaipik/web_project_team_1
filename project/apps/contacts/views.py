from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages

from apps.contacts.forms import ContactForm
from apps.contacts.models import Contact


def add_contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(
                request, messages.INFO, "A new contact added successfully!"
            )
            return redirect(to="contacts:main")
        else:
            return render(request, "contacts/contact_form.html", {"form": form})

    form = ContactForm()
    return render(request, "contacts/contact_form.html", {"form": form})


def update_contact(request, id):
    if request.method == "POST":
        contact = Contact.objects.get(id=id)
        form = ContactForm(request.POST, instance=contact)
        if form.is_valid():
            form.save()
            messages.add_message(
                request, messages.INFO, "A new contact added successfully!"
            )
            return redirect(to="contacts:main")
        else:
            return JsonResponse(
                {
                    "errors": dict(form.errors.items()),
                }
            )


def delete_contact(request, id):
    contact = Contact.objects.get(id=id)
    contact.delete()
    messages.add_message(request, messages.INFO, "Deleted successfully!")
    return redirect(to="contacts:main")
