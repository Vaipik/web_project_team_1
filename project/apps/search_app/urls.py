from django.urls import re_path

from .views import SearchUniView, SearchContactView, SearchFileView

app_name = "search_app"

urlpatterns = [
    re_path(r"^files.+search$", SearchFileView.as_view(), name="search_files"),
    re_path(r"^contacts.+search$", SearchContactView.as_view(), name="search_contacts"),
    # """this path must be at the end"""
    re_path(r"^.*search$", SearchUniView.as_view(), name="search_results"),
]
