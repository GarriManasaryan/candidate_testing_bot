from bot_base.bot_main import *

@bot.message_handler(content_types=['text'])
def echo_all(message):
    try:
        if message.text == 'x':
            bot.send_message(call.chat.id, "Hello!")

        elif message.text == 'y':
            try:
                bot.send_message(message.chat.id, test_json.get('data'))

            except Exception as e:
                exception_name = (type(e).__name__)
                bot.send_message(message.chat.id, "Something went wrong")
                bot.send_message(message.chat.id, f'{exception_name}: {e}')

    except Exception as e:
        print(a)
        print(repr(e))
        exception_name = (type(e).__name__)
        bot.send_message(message.from_user.id, "Something went wrong")
        bot.send_message(message.from_user.id, f'{exception_name}: {e}')
