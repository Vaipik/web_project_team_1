from django import forms
from django.contrib.admin.widgets import AdminSplitDateTime


class SenderSettingsForm(forms.Form):
    # TODO make form ckecklist for sender choice
    event = forms.CharField(max_length=64)
    message = forms.CharField(max_length=250)
    # date_input = forms.DateField(widget=AdminDateWidget())
    # time_input = forms.TimeField(widget=AdminTimeWidget())
    date_time_input = forms.SplitDateTimeField(label='Date time to remind about task', widget=AdminSplitDateTime())
