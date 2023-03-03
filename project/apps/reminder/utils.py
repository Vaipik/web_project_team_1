import json
from uuid import uuid4

from django_celery_beat.models import PeriodicTask, ClockedSchedule


def add_scheduled_bot_message(**kwargs):
    clocked = ClockedSchedule(clocked_time=kwargs['date_time_input'])
    clocked.save()

    name_exist = PeriodicTask.objects.filter(name=kwargs['event'])

    if name_exist:
        name = kwargs['event'] + "/" + str(uuid4())
    else:
        name = kwargs['event']

    PeriodicTask.objects.create(name=name,
                                task="telegram_msg_bot",
                                clocked=clocked,
                                one_off=True,
                                args=json.dumps([f"{kwargs['message']}", ])
                                )
