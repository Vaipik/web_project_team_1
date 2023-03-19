import json
from uuid import uuid4

from django_celery_beat.models import PeriodicTask, ClockedSchedule

from ..models import TaskReminder, TaskSender, Sender


def get_periodic_task_name(event, sender_name) -> str:
    event_name = event + "/" + sender_name
    name_exist = PeriodicTask.objects.filter(name=event_name).all()

    if name_exist:
        name = event_name + "/" + str(uuid4())
    else:
        name = event_name

    return name


def add_clocked_message_by_sender(sender_name: str, worker_name: str, **kwargs):
    clocked = ClockedSchedule(clocked_time=kwargs['date_time_input'])
    clocked.save()

    periodic = PeriodicTask.objects.create(name=get_periodic_task_name(kwargs['event'], sender_name),
                                           task=worker_name,
                                           clocked=clocked,
                                           one_off=True,
                                           kwargs=json.dumps(
                                               {
                                                   "message": f"{kwargs['message']}",
                                                   "user_id": kwargs["user"].pk,
                                               })
                                           )

    return periodic


def add_reminder_tasks(**kwargs):
    task_name = TaskReminder.objects.create(task_name=kwargs["event"],
                                            user=kwargs["user"])

    senders = kwargs['senders']
    for sender in senders:
        periodic = add_clocked_message_by_sender(**kwargs,
                                                 sender_name=sender.name,
                                                 worker_name=sender.name.lower() + "_msg_sender")
        TaskSender.objects.create(task_name=task_name, sender=sender, periodic_task=periodic)


def update_reminder_tasks(**kwargs):
    task_name = TaskReminder.objects.filter(uuid=kwargs['uuid'], user=kwargs["user"]).first()

    task_name.task_name = kwargs["event"]

    assigned_senders = set(Sender.objects.filter(tasksender__task_name=task_name).all())
    new_senders = set(kwargs['senders'])

    senders_for_delete = assigned_senders.difference(new_senders)
    senders_for_create = new_senders.difference(assigned_senders)
    senders_for_update = assigned_senders.intersection(new_senders)

    for sender in senders_for_delete:
        tasksender = TaskSender.objects.filter(task_name=task_name, sender=sender).first()
        tasksender.periodic_task.delete()

    for sender in senders_for_create:
        periodic = add_clocked_message_by_sender(**kwargs,
                                                 sender_name=sender.name,
                                                 worker_name=sender.name.lower() + "_msg_sender")
        TaskSender.objects.create(task_name=task_name, sender=sender, periodic_task=periodic)

    for sender in senders_for_update:
        task_sender = TaskSender.objects.filter(task_name=task_name,
                                                sender=sender).first()

        update_clocked_message_by_sender(periodic=task_sender.periodic_task,
                                         sender_name=sender.name,
                                         event=kwargs["event"],
                                         message=kwargs["message"],
                                         user_id=kwargs["user"].pk,
                                         dt=kwargs["date_time_input"],
                                         )

    task_name.save()

    return task_name


def update_clocked_message_by_sender(periodic, sender_name, event, message, user_id, dt):

    periodic.name = get_periodic_task_name(event, sender_name)
    periodic.kwargs = json.dumps({"message": message, "user_id": user_id})

    periodic.clocked.clocked_time = dt
    periodic.clocked.save()

    periodic.save()


def delete_task_reminder(object_):
    tasks = PeriodicTask.objects.filter(periodictasks__task_name=object_).all()
    [task.clocked.delete() for task in tasks]
    [task.delete() for task in tasks]
    object_.delete()


def event_name_exist(event_name, user) -> bool:
    if TaskReminder.objects.filter(task_name=event_name, user=user).all():
        return True
    return False


def event_name_exist_edit(pk, event_name, user) -> bool:
    if TaskReminder.objects.filter(task_name=event_name, user=user).exclude(pk=pk).all():
        return True
    return False
