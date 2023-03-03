import os

from celery import shared_task

from utils.telegramm.telegram_bot import send_custom_message


@shared_task(name='telegram_msg_bot')
def telegram_msg_bot(message):
    send_custom_message(int(os.environ.get('TELEGRAM_CHAT_ID')), message)
    return True
