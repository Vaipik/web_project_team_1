## Steps how to start project

1. Python 3.10
2. Install poetry
3. Run `poetry install` in `project_name_directory`
4. In `maindir` create `.env` file where you need to you need to specify following:
    * SECRET_KEY=`your secret key`
    * DB_NAME=`db name`
    * DB_USER=`db user`
    * DB_PASSWORD=`db password`
    * DB_PORT=`db port`
    * DROPBOX_APP_KEY=`dropbox app key`
    * DROPBOX_APP_SECRET=`dropbox app secret`
    * DROPBOX_OAUTH2_REFRESH_TOKEN=`dropbox refresh token`
    * DROPBOX_ROOT_PATH=`dropbox root path where files will be uploaded`
5. Run `docker-compose up -d --build` and visit `127.0.0.1:8000` to start using

Py7WebProject

https://www.dropbox.com/oauth2/authorize?client_id=619zg49xua7barp&token_access_type=offline&response_type=code

curl https://api.dropbox.com/oauth2/token -d code=tqLkjb6TzhAAAAAAAAAAQYRP5kVAKcWTlkqiTD1xqIo -d
grant_type=authorization_code -u 619zg49xua7barp:d5elt0ogmef68rf

{'_state': <django.db.models.base.ModelState object at 0x7f63e3574f40>, 
'id': 9, 
'name': '369852147', 
'task': 'apps.reminder.tasks.telegram_msg_bot', 
'interval_id': None, 
'crontab_id': None, 
'solar_id': None, 
'clocked_id': 9, 
'args': ['qazwsxedcrfvtgb'], 
'kwargs': '{}', 
'queue': None, 
'exchange': None, 
'routing_key': None, 
'headers': '{}', 
'priority': None, 
'expires': None, 
'expire_seconds': None, 
'one_off': True, 
'start_time': None, 
'enabled': True, 
'last_run_at': None, 
'total_run_count': 0, 
'date_changed': datetime.datetime(2023, 3, 1, 14, 22, 12, 933187, tzinfo=datetime.timezone.utc), 
'description': ''}


{'_state': <django.db.models.base.ModelState object at 0x7fd6576accd0>, 'id': 11, 'name': 'сообщение в телеграм', 'task': 'apps.reminder.tasks.telegram_msg_bot', 'interval_id': None, 'crontab_id': None, 'solar_id': None, 'clocked_id': 11, 'args': ['сообщение для сравнения'], 'kwargs': '{}', 'queue': None, 'exchange': None, 'routing_key': None, 'headers': '{}', 'priority': None, 'expires': None, 'expire_seconds': None, 'one_off': True, 'start_time': None, 'enabled': True, 'last_run_at': None, 'total_run_count': 0, 'date_changed': datetime.datetime(2023, 3, 1, 14, 36, 54, 587178, tzinfo=datetime.timezone.utc), 'description': ''}
{'_state': <django.db.models.base.ModelState object at 0x7fd6576acdf0>, 'id': 9,  'name': '369852147',             'task': 'apps.reminder.tasks.telegram_msg_bot', 'interval_id': None, 'crontab_id': None, 'solar_id': None, 'clocked_id': 9, 'args': '["qazwsxedcrfvtgb"]',        'kwargs': '{}', 'queue': None, 'exchange': None, 'routing_key': None, 'headers': '{}', 'priority': None, 'expires': None, 'expire_seconds': None, 'one_off': True, 'start_time': None, 'enabled': True, 'last_run_at': None, 'total_run_count': 0, 'date_changed': datetime.datetime(2023, 3, 1, 14, 36, 2, 228655, tzinfo=datetime.timezone.utc), 'description': ''}