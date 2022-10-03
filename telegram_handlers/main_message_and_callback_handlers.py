from bot_base.bot_main import *
from telegram_handlers.error_handlers import *
from services.google_service import *
from time import sleep

with open(os.path.join(os.getcwd(), 'spam_defender', 'banned_list.json')) as f:
    banned_list = json.load(f) # add another list for already passed candidates

# connect to drive and google_sheets
# gsr = GoogleServiceHandler()
spam_counter = {}

@bot.message_handler(content_types=['text'])
@message_error_handler()
def welcome(message):
    if message.chat.id in banned_list:
        bot.send_message(message.chat.id, 'Sorry, but you\'ve been banned for spamming; contact your HR coordinator for further instructions')
    else:
        text = message.text

        if text == '/start':
            clicked = spam_counter.get(message.chat.id, 0)
            spam_counter[message.chat.id] = clicked + 1

            if spam_counter.get(message.chat.id) > 5:
                bot.send_message(message.chat.id, 'Sorry, but you\'ve been banned for spamming; contact your HR coordinator for further instructions')

                with open(os.path.join(os.getcwd(), 'spam_defender', 'banned_list.json'), 'w') as f:
                    banned_list.append(message.chat.id)
                    json.dump(banned_list, f)

            else:
                msg = bot.send_message(message.chat.id, f'Welcome to {company} Candidates\' Assessment System! Before we begin, send me your token (candidate_id) like this:\ncand-xx-00000000-xx-0000-000000000000')
                bot.register_next_step_handler(msg, process_token_from_candidate)

        # elif text == 'z':
        #     os._exit(0)


@message_error_handler()
def process_token_from_candidate(message):
    token = message.text
    bot.send_message(message.chat.id, f'Verifying token, just a moment')
    sleep(1)
    df_all_candidates, worksheet_canidate = gsr.get_google_sheet_df()
    all_tokens = set(df_all_candidates['token'])

    # if token in + already proccessed
