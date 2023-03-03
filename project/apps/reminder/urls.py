from django.urls import re_path

from .views import CalendarView

app_name = "reminder"


urlpatterns = [
    re_path(r"^reminder$", CalendarView.as_view(), name="calendar"),
]
