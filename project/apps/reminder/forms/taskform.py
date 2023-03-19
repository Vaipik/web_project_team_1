import copy
import json

from django import forms

from django.contrib.admin.widgets import AdminSplitDateTime
from django.core.exceptions import ValidationError

from ..models import Sender


class AddTaskForm(forms.Form):
    event = forms.CharField(max_length=64)
    message = forms.CharField(max_length=250)
    date_time_input = forms.SplitDateTimeField(label='Date time to remind about task', widget=AdminSplitDateTime())
    senders = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                             queryset=Sender.objects.none(),
                                             )

    def __init__(self, user=None, *args, **kwargs):
        self.object = None

        keywordargs = copy.deepcopy(kwargs)
        if 'instance' in keywordargs.keys():
            keywordargs.pop('instance')
        super().__init__(*args, **keywordargs)

        if user:
            self.fields["senders"].queryset = Sender.objects.filter(subscription__user=user).all()

        if 'instance' in kwargs.keys():
            self._initial_form(kwargs['instance'])

    def clean(self):
        cleaned_data = super(AddTaskForm, self).clean()
        senders = cleaned_data.get('senders')
        if not senders:
            raise ValidationError("You can add or change accessible senders in settings")

        return cleaned_data

    def _initial_form(self, task):
        self.fields['event'].initial = task.task_name

        periodic_task = task.periodic_tasks.first()
        kwargs = json.loads(periodic_task.kwargs)
        self.fields['message'].initial = kwargs["message"]
        self.fields['date_time_input'].initial = periodic_task.clocked.clocked_time

        assigned_senders = Sender.objects.filter(tasksender__task_name=task).all()
        choices = [obj_ for obj_, _ in self.fields['senders'].choices if obj_.instance in assigned_senders]
        self.fields['senders'].initial = choices

    def save(self):
        return self.object
