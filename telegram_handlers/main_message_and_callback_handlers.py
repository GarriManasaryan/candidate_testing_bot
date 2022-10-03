from bot_base.bot_main import *
from telegram_handlers.error_handlers import *

@bot.message_handler(content_types=['text'])
@message_error_handler()
def echo_all(message):
    if message.text == 'x':
        bot.send_message(call.chat.id, "Hello!")

    elif message.text == 'y':
        bot.send_message(message.chat.id, 'sdc')
