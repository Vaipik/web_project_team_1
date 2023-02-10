from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from apps.contacts.models import Contact


@login_required
def delete_contact(request, pk):
    Contact.objects.get(pk=pk, owner=request.user).delete()
    messages.add_message(request, messages.INFO, "Deleted successfully!")
    return redirect(to="contacts:contacts")
