from telegram_handlers.main_message_and_callback_handlers import *
print('All libs imported successfully')

@bot_priest()
def main():
    bot.polling(none_stop=True, interval=0, timeout=125)

if __name__ == '__main__':
    main()
    # gsr = GoogleServiceHandler()
    # gsr.excel_downloader_from_drive("1uTfz3HljB5naVr46Dd14Iz7zYxad70hcjBciLru8bsU", "opcapo")