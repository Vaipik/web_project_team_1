from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory

from apps.contacts.forms import ContactForm, EmailForm, PhoneForm
from apps.contacts.models import Email, Contact, Phone


@login_required
def add_contact(request):
    """
    Adds new contacts to the contact book.
    """
    contact_form = ContactForm(prefix="cont_form")
    EmailFormSet = inlineformset_factory(
        parent_model=Contact,
        model=Email,
        form=EmailForm,
        fields="__all__",
        extra=2,
        can_delete=True,
    )
    PhoneFormSet = inlineformset_factory(
        parent_model=Contact,
        model=Phone,
        form=PhoneForm,
        fields="__all__",
        extra=2,
        can_delete=True,
    )

    if request.method == "POST":
        contact_form = ContactForm(request.POST, prefix="cont_form")
        email_forms = EmailFormSet(request.POST, prefix="email_form")
        phone_forms = PhoneFormSet(request.POST, prefix="phone_form")
        if (
            contact_form.is_valid()
            and email_forms.is_valid()
            and phone_forms.is_valid()
        ):
            contact_form.instance.owner = request.user
            contact = contact_form.save()

            deleted_emails = email_forms.deleted_forms
            for email_form in email_forms:
                if email_form not in deleted_emails:
                    email_form.instance.owner = contact
                    email_form.save()

            deleted_phones = phone_forms.deleted_forms
            for phone_form in phone_forms:
                if phone_form not in deleted_phones:
                    phone_form.instance.owner = contact
                    phone_form.save()
            messages.add_message(
                request, messages.INFO, "A new contact added successfully!"
            )
            return redirect(to="contacts:contacts")
        else:
            return render(
                request,
                "contacts/contact_add.html",
                {
                    "cont_form": contact_form,
                    "email_form": email_forms,
                    "phone_form": phone_forms,
                },
            )

    return render(
        request,
        "contacts/contact_add.html",
        {
            "cont_form": contact_form,
            "email_form": EmailFormSet(prefix="email_form"),
            "phone_form": PhoneFormSet(prefix="phone_form"),
        },
    )
