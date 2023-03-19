from django.urls import reverse_lazy

from .forms import AddTaskForm


class ReminderMixin:
    template_name = "reminder/pages/add_task.html"
    pk_url_kwarg = "task_uuid"
    form_class = AddTaskForm
    success_url = reverse_lazy("reminder:reminder_task_list")

    def get_form(self, form_class=None):
        """override base method, add user to args"""
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(self.request.user, **self.get_form_kwargs())

