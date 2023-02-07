from django.urls import re_path

from .views import SearchUniView

app_name = "search_app"

urlpatterns = [
    re_path(r"^.*search$", SearchUniView.as_view(), name="search_results"),
]
