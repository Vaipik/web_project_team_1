from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import FormView, ListView, DeleteView, UpdateView

from .forms import SenderSettingsForm
from .models.taskreminder import TaskReminder
from .reminder_mixin import ReminderMixin
from .services.taskreminder import add_reminder_tasks, update_reminder_tasks, delete_task_reminder, event_name_exist, \
    event_name_exist_edit
from utils.pagination import PaginationMixin


class ReminderTaskView(LoginRequiredMixin, PaginationMixin, ListView):
    template_name = 'reminder/pages/reminder_task_list.html'
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update(
            **self.get_pages(page_obj=context["page_obj"]),
        )
        return context

    def get_queryset(self):
        tasks = TaskReminder.objects.filter(user=self.request.user).all()
        return tasks


class AddTaskView(LoginRequiredMixin, ReminderMixin, FormView):
    submit_url = "reminder:add_task"
    extra_context = {"title": "Add task", "submit_url": submit_url}

    def form_valid(self, form):
        data = form.cleaned_data
        if event_name_exist(data["event"], self.request.user):
            form.add_error(field="event", error="Event name already exists. Please rename event.")
            return super().form_invalid(form)
        add_reminder_tasks(**data, user=self.request.user)
        return super().form_valid(form)


class EditTaskView(LoginRequiredMixin, ReminderMixin, UpdateView):
    submit_url = "reminder:edit_task"
    extra_context = {"title": "Edit task", "submit_url": submit_url}

    def get_queryset(self):
        task = TaskReminder.objects.filter(pk=self.kwargs['task_uuid'])
        return task

    def form_valid(self, form):
        data = form.cleaned_data
        if event_name_exist_edit(self.kwargs["task_uuid"], data["event"], self.request.user):
            form.add_error(field="event", error="Another event name already exists. Please rename event.")
            return super().form_invalid(form)
        form.object = update_reminder_tasks(**data, user=self.request.user, uuid=self.kwargs["task_uuid"])
        return super().form_valid(form)


class DeleteTaskView(LoginRequiredMixin, DeleteView):
    pk_url_kwarg = "task_uuid"
    model = TaskReminder
    success_url = reverse_lazy("reminder:reminder_task_list")

    def form_valid(self, form):
        success_url = self.get_success_url()
        delete_task_reminder(self.object)
        return HttpResponseRedirect(success_url)


class SenderSettingsView(LoginRequiredMixin, FormView):
    # TODO make sender_settings page
    template_name = 'reminder/pages/sender_settings.html'
    form_class = SenderSettingsForm
    extra_context = {"title": "Sender settings"}
    success_url = reverse_lazy("reminder:reminder_task_list")

    def form_valid(self, form):
        data = form.cleaned_data

        return super().form_valid(form)


