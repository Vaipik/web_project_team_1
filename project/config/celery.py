import os

from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


# from celery.signals import worker_process_init, worker_process_shutdown
#
# db_conn = None
#
#
# @worker_process_init.connect
# def init_worker(**kwargs):
#     global db_conn
#     print('Initializing database connection for worker.')
#     db_conn = db.connect(DB_CONNECT_STRING)
#
#
# @worker_process_shutdown.connect
# def shutdown_worker(**kwargs):
#     global db_conn
#     if db_conn:
#         print('Closing database connectionn for worker.')
#         db_conn.close()
