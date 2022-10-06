from bot_base.bot_main import *
from telegram_handlers.error_handlers import *
from services.google_service import *
from time import sleep

# connect to drive and google_sheets
gsr = GoogleServiceHandler()

spam_counter = {}
@bot.message_handler(content_types=['text'])
@message_error_handler()
def welcome(message):
    chat_id = message.chat.id

    if chat_id in banned_list:
        bot.send_message(chat_id, banned_message)

    else:
        text = message.text

        if text == 'e':
            os._exit(0)

        elif text == 'tset':
            # gsr.docs_downloader_from_drive(fileId = 'https://docs.google.com/document/d/1XwkUaq0hvAjWlzzl2D5t-tgQKAUEHYw7_q3A9vSuG6Y/edit'.split('/')[-2])
            bot.send_document(chat_id = chat_id, document = open(os.path.join(path_to_download, 'Task.docx'), 'rb'), caption = 'caption', parse_mode='html')

        elif text == '/start':
            clicked = spam_counter.get(chat_id, 0)
            spam_counter[chat_id] = clicked + 1

            if spam_counter.get(chat_id) > 5:
                bot.send_message(chat_id, banned_message)

                with open(os.path.join(os.getcwd(), 'spam_defender', 'banned_list.json'), 'w') as f:
                    banned_list.append(chat_id)
                    json.dump(banned_list, f)

            else:
                msg = bot.send_message(chat_id, f'Welcome to {company} Candidates\' Assessment System! Before we begin, send me your token (candidate_id) like this:\ncand-xx-00000000-xx-0000-000000000000')
                bot.register_next_step_handler(msg, process_token_from_candidate)

@message_error_handler()
def process_token_from_candidate(message):
    token = message.text
    chat_id = message.chat.id

    bot.send_message(chat_id, f'Verifying token, just a moment')
    sleep(1)

    df_all_candidates = gsr.get_google_sheet_df()
    all_tokens = set(df_all_candidates['token'])

    if not token in all_tokens:
        bot.send_message(chat_id, f'Invalid token, permission denied; {further_instructions_message}')

    else:
        df_candidate = df_all_candidates[df_all_candidates['token'] == token]
        candidate_info_dict = df_candidate.to_dict('records')[0]
        bot.send_message(chat_id, f'Perfect, downloading test files...')
        try:
            gsr.docs_downloader_from_drive(fileId = candidate_info_dict.get('Link_to_docx_task').split('/')[-2])
            bot.send_document(chat_id = chat_id, document = open(os.path.join(path_to_download, 'Task.docx'), 'rb'), caption = 'caption', parse_mode='html')
        except:
            bot.send_message(chat_id, f'Something went wrong while donwloading your tasks; {further_instructions_message}')
