from bot_base.bot_main import *
from logs.custom_logger import *

def get_chat_id_from_call_or_msg(message_or_call):
    try:
        chat_id = message_or_call.message.chat.id # call obj
    except:
        chat_id = message_or_call.chat.id # message obj

    return chat_id

def message_error_handler():

    def message_error_handler_wrapper(func):

        def wrapper_func(*args, **kwargs):
            message_or_call = args[0]
            try:
                logger(message_or_call)
                result = func(*args, **kwargs)

                return result

            except Exception as e:

                chat_id = get_chat_id_from_call_or_msg(message_or_call)

                exception_name = (type(e).__name__)
                logger(message_or_call, repr(e))
                bot.send_message(chat_id, "Something went wrong")
                bot.send_message(chat_id, f'{exception_name}: {e}')

        return wrapper_func

    return message_error_handler_wrapper
