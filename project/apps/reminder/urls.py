from django.urls import re_path, path

from .views import AddTaskView, ReminderTaskView, SenderSettingsView, DeleteTaskView, EditTaskView

app_name = "reminder"


urlpatterns = [
    path("delete/<uuid:task_uuid>/", DeleteTaskView.as_view(), name="delete_task"),
    path("edit/<uuid:task_uuid>/", EditTaskView.as_view(), name="edit_task"),
    path("", ReminderTaskView.as_view(), name="reminder_task_list"),
    re_path(r"^add_task$", AddTaskView.as_view(), name="add_task"),
    re_path(r"^sender_settings$", SenderSettingsView.as_view(), name="sender_settings"),
]
