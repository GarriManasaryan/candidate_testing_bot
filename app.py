from handlers.main_message_and_callback_handlers import *
bot.polling(none_stop=True, interval=0, timeout=125) # might be the problem of failing → increase timeout (prev value=0)
