from django.contrib import admin

# Register your models here.
from .models.taskreminder import Sender, SenderSubscription, TaskReminder

admin.site.register(Sender)
admin.site.register(SenderSubscription)
admin.site.register(TaskReminder)
