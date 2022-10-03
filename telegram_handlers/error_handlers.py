from bot_base.bot_main import *

def message_error_handler():

    def message_error_handler_wrapper(func):

        def wrapper_func(*args, **kwargs):

            try:
                result = func(*args, **kwargs)
                return result

            except Exception as e:
                message = args[0]
                exception_name = (type(e).__name__)
                bot.send_message(message.chat.id, "Something went wrong")
                bot.send_message(message.chat.id, f'{exception_name}: {e}')

        return wrapper_func

    return message_error_handler_wrapper
