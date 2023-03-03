from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import FormView

from .forms import CalendarForm
from .tasks import telegram_msg_bot
from .utils import add_scheduled_bot_message


class CalendarView(LoginRequiredMixin, FormView):
    template_name = 'reminder/calendar.html'
    form_class = CalendarForm
    extra_context = {"title": "Calendar"}
    success_url = reverse_lazy("reminder:calendar")

    def form_valid(self, form):
        data = form.cleaned_data
        add_scheduled_bot_message(**data)

        return super().form_valid(form)
