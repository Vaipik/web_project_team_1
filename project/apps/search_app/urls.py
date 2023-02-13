from django.urls import re_path

from .views import SearchUniView, SearchContactView, SearchFileView, SearchNoteView

app_name = "search_app"

urlpatterns = [
    re_path(r"^contacts.+search$", SearchContactView.as_view(), name="search_contacts"),
    re_path(r"^files.+search$", SearchFileView.as_view(), name="search_files"),
    re_path(r"^notes.+search$", SearchNoteView.as_view(), name="search_notes"),
    # """this path must be at the end"""
    re_path(r"^.*search$", SearchUniView.as_view(), name="search_results"),
]
