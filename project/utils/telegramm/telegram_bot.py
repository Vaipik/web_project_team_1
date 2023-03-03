import os

import telebot

API_TOKEN = os.environ.get("TELEGRAM_API_TOKEN")

bot = telebot.TeleBot(API_TOKEN)


# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, """\
Hi there, I am EchoBot.
I am here to echo your kind words back to you. Just say anything nice and I'll say the exact same thing to you!\
""")


# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def echo_message(message: telebot.types.Message):
    send_custom_message(message.chat.id, message.text)

    bot.reply_to(message, message.text)


def send_custom_message(chat_id, message):
    bot.send_message(chat_id, message)


if __name__ == '__main__':
    bot.infinity_polling()
