from django.urls import re_path

from .views import SearchNotesView, SearchContactsView, SearchTempContactView

app_name = "search_app"

urlpatterns = [
    re_path(r"^auth.+search$", SearchTempContactView.as_view(), name="search_notes"),  # route for testing
    re_path(r"^notes.+search$", SearchNotesView.as_view(), name="search_notes"),
    re_path(r"^contacts.+search$", SearchContactsView.as_view(), name="search_contacts"),
]
