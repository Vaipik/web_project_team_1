from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
from django.views.generic import ListView

from .models import TempNote, TempContact
from .utils import SearchAppMixin
from ..contacts.models import Contact


class SearchNotesView(LoginRequiredMixin, SearchAppMixin, ListView):
    model = TempNote
    template_name = "search_app/search_notes.html"
    search_fields = [
        "description",
        "text",
        "tags"
    ]


class SearchTempContactView(LoginRequiredMixin, SearchAppMixin, ListView):
    model = TempContact
    template_name = "search_app/search_notes.html"
    search_fields = [
        "description",
        "text",
        "tags"
    ]


class SearchContactsView(LoginRequiredMixin, SearchAppMixin, ListView):
    model = Contact
    template_name = "search_app/search_contacts.html"
    search_fields = [
        "name",
        "address",
        "phones"
    ]
