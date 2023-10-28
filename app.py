from telegram_handlers.main_message_and_callback_handlers import *
print('All libs imported successfully')

@bot_priest()
def main():
    bot.polling(none_stop=True, interval=0, timeout=125)

if __name__ == '__main__':
    main()
