from django.shortcuts import render, redirect
from django.contrib import messages

from forms import ContactForm


def main(request):
    return render(request, 'contacts/contact_book.html', {})


def add_contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO, 'A new contact added successfully!')
            return redirect(to='contacts:main')
        else:
            messages.add_message(request, messages.ERROR, 'Some info is invalid.')
            return redirect(to='contacts:add_contact')

    return render(request, 'contacts/contact_form.html', {"form": ContactForm()})
