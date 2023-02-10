from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory

from apps.contacts.forms import ContactForm, EmailForm, PhoneForm
from apps.contacts.models import Contact, Email, Phone


@login_required
def update_contact(request, pk):
    """
    Updates person's data.
    """
    contact = Contact.objects.get(pk=pk, owner=request.user)
    EmailsFormSet = inlineformset_factory(
        parent_model=Contact, model=Email, form=EmailForm, fields="__all__", extra=1
    )
    PhonesFormSet = inlineformset_factory(
        parent_model=Contact, model=Phone, form=PhoneForm, fields="__all__", extra=1
    )
    if request.method == "POST":
        contact_form = ContactForm(
            request.POST,
            instance=contact,
            prefix="cont_form",
        )
        emails_form = EmailsFormSet(
            request.POST,
            instance=contact,
            prefix="email_form",
        )
        phones_form = PhonesFormSet(
            request.POST,
            instance=contact,
            prefix="phone_form",
        )
        if (
            contact_form.is_valid()
            and emails_form.is_valid()
            and phones_form.is_valid()
        ):
            contact.save()
            emails_form.save()
            phones_form.save()
            messages.add_message(
                request, messages.INFO, "The contact updated successfully!"
            )
            return redirect(to="contacts:contacts")
        else:
            return render(
                request,
                "contacts/contact_update.html",
                {
                    "contact": contact,
                    "cont_form": contact_form,
                    "email_form": emails_form,
                    "phone_form": phones_form,
                },
            )

    return render(
        request,
        "contacts/contact_update.html",
        {
            "contact": contact,
            "cont_form": ContactForm(prefix="cont_form", instance=contact),
            "email_form": EmailsFormSet(prefix="email_form", instance=contact),
            "phone_form": PhonesFormSet(prefix="phone_form", instance=contact),
        },
    )
