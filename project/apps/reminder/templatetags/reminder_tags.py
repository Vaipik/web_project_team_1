import json

from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(name='get_msg')
def get_msg(tasks) -> str:
    task = tasks.first()
    kwargs = json.loads(task.kwargs)
    return mark_safe(kwargs["message"])


@register.filter(name='get_datetime')
def get_datetime(tasks) -> str:
    task = tasks.first()
    dt = task.clocked.clocked_time
    return mark_safe(dt.strftime("%d %B, %Y %H:%m"))


@register.filter(name='get_senders')
def get_senders(senders) -> str:
    sender_list = [sender.name for sender in senders.all()]
    return mark_safe(f"{sender_list}".strip("[]"))
