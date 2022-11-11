from bot_base.bot_main import *
from telegram_handlers.error_handlers import *
from services.google_service import *
from time import sleep
from datetime import datetime, timedelta

# connect to drive and google_sheets
gsr = GoogleServiceHandler()
spam_counter = {}

@bot.message_handler(content_types=['text'])
@message_error_handler()
def welcome(message):
    chat_id = message.chat.id

    if chat_id in banned_list:
        bot.send_message(chat_id, banned_message)

    elif chat_id in already_processed_users:
        bot.send_message(chat_id, old_users)

    else:
        text = message.text

        if text == 'test':
            bot.send_message(chat_id, 'test')

        elif text == '/start':
            clicked = spam_counter.get(chat_id, 0)
            spam_counter[chat_id] = clicked + 1

            if spam_counter.get(chat_id) > 5:
                old_user_handler(chat_id, 'banned_list')
                bot.send_message(chat_id, banned_message)

            else:
                msg = bot.send_message(chat_id, welcome_message)
                bot.register_next_step_handler(msg, process_token_from_candidate)

def old_user_handler(user_chat_id, old_user_reason_list):
    with open(os.path.join(os.getcwd(), 'spam_defender', f'{old_user_reason_list}.json'), 'w') as f:
        source_list = banned_list if old_user_reason_list == 'banned_list' else already_processed_users
        source_list.append(user_chat_id)
        json.dump(source_list, f)

@message_error_handler()
def process_token_from_candidate(message):
    token = message.text
    chat_id = message.chat.id

    bot.send_message(chat_id, verifying_token)
    sleep(1)

    df_all_candidates = gsr.get_google_sheet_df()
    all_tokens = set(df_all_candidates['token'])

    if not token in all_tokens:
        bot.send_message(chat_id, invalid_token)

    else:
        df_candidate = df_all_candidates[df_all_candidates['token'] == token]
        candidate_info_dict = df_candidate.to_dict('records')[0]
        candidate_info_dict['submitted_excel_answer'] = True if candidate_info_dict['Send_excel_test_too'] != 'Yes' else False
        candidate_info_dict['submitted_docx_answer'] = False

        token_end = token.split('-')[-1]

        process_candidate_temp_info(token_end, 'save_dict', candidate_info_dict)

        bot.send_message(chat_id, file_download)

        try:
            fileId = candidate_info_dict.get('Link_to_docx_task').split('/')[-2]
            gsr.docs_downloader_from_drive(fileId = fileId)

            markup = InlineKeyboardMarkup(row_width=2)
            markup.add(InlineKeyboardButton('Start', callback_data=f'start_the_test_{token_end}')) # removing token might lead to concurrency issues: one user calls functions, overwriting prev calls and reminders

            if candidate_info_dict.get('Send_excel_test_too') == 'Yes':
                bot.send_message(chat_id, full_task_instr, parse_mode='html', reply_markup=markup)

            else:
                bot.send_message(chat_id, just_clinical_task_instr, parse_mode='html', reply_markup=markup)

        except:
            bot.send_message(chat_id, error_downloading_files)

def process_candidate_temp_info(token_end, mode = 'get_all', candidate_dict = 'provided_with_save_mode', file_name = 'provided_with_files_mode'):
    path_to_file = os.path.join(os.getcwd(), 'temp_files', f'user_{token_end}.json')

    if mode == 'get_all':
        with open(path_to_file) as f:
            return json.load(f)

    elif mode == 'save_dict':
        with open(path_to_file, 'w') as f:
            json.dump(candidate_dict, f, indent = 2)

    elif mode in ['excel', 'docx']:
        with open(path_to_file) as f:
            candidate_dict = json.load(f)

        candidate_dict[f'submitted_{mode}_answer'] = True
        candidate_dict[f'{mode}_file_name'] = file_name

        with open(path_to_file, 'w') as f:
            json.dump(candidate_dict, f, indent = 2)

@message_error_handler()
def time_left_reminder(message_or_call, excel_finish_time, token_end, time_left_text):
    date_now = datetime.now()
    while excel_finish_time > date_now:
        date_now = datetime.now()
        sleep(60)

    # check if the answer is already submitted. If so, dont send time left message
    candidate_info_dict = process_candidate_temp_info(token_end)
    already_submitted_excel_answer = candidate_info_dict['submitted_excel_answer']

    if not already_submitted_excel_answer:
        chat_id = get_chat_id_from_call_or_msg(message_or_call)
        bot.send_message(chat_id, time_left_text, parse_mode='html')

def upload_to_google_folder_when_finished(token_end):
    candidate_info_dict = process_candidate_temp_info(token_end)
    excel_already_sent = candidate_info_dict['submitted_excel_answer']
    docx_already_sent = candidate_info_dict['submitted_docx_answer']

    if excel_already_sent and docx_already_sent:
        # create candidate folder in google drive
        team_parent_folder_id = credentials['teams'][candidate_info_dict['CIT_department']]
        folder_name = candidate_info_dict['Last_name'] + '_' + candidate_info_dict['First_name']
        res_candidate_folder_id = gsr.create_google_folder(team_parent_folder_id, folder_name).get('id')
        candidate_info_dict['Link_to_candidate_google_folder'] = f'https://drive.google.com/drive/u/0/folders/{res_candidate_folder_id}'

        # upload files
        for key, value in candidate_info_dict.items():
            if 'file_name' in key:
                file_name = value
                file_full_path = os.path.join(os.getcwd(), 'downloaded_tasks', file_name)
                mimetype = key.split('_')[0]

                sleep(5)
                gsr.add_file_to_google_folder(res_candidate_folder_id, file_name, file_full_path, mimetype)

@message_error_handler()
def get_file_msg(message, token_end, mode):
    candidate_info_dict = process_candidate_temp_info(token_end)
    first_name = candidate_info_dict.get('First_name', 'First_name')
    last_name = candidate_info_dict.get('Last_name', 'Last_name')

    file_name = '_'.join([last_name, first_name, token_end[:4], message.document.file_name])

    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    with open(os.path.join(path_to_download, file_name), 'wb') as new_file:
        new_file.write(downloaded_file)

    process_candidate_temp_info(token_end, mode, file_name = file_name)
    bot.send_message(message.chat.id, success_answer_saved)

    upload_to_google_folder_when_finished(token_end)

@bot.callback_query_handler(func=lambda call: True)
@message_error_handler()
def callback_handler(call):

    if call.message:
        chat_id = call.message.chat.id

        if chat_id in already_processed_users or chat_id in banned_list:
            bot.send_message(chat_id, old_users)

        else:
            token_end = str(call.data).split('_')[-1]

            candidate_info_dict = process_candidate_temp_info(token_end)

            excel_test_too_flag = candidate_info_dict.get('Send_excel_test_too')

            if 'start_the_test' in str(call.data):

                excel_finish_time_30_min_reminder = datetime.now() + timedelta(hours = timedelta_time_left_30_min)
                excel_finish_time_5_min_reminder = datetime.now() + timedelta(hours = timedelta_time_left_5_min)

                if excel_test_too_flag == 'Yes':
                    bot.send_document(chat_id = chat_id, document = open(os.path.join(path_to_download, 'Excel_task.xlsx'), 'rb'), caption = instruction_time_limit_excel, parse_mode='html')

                bot.send_document(chat_id = chat_id, document = open(os.path.join(path_to_download, 'Clinical_task.docx'), 'rb'), caption = instruction_time_limit_clinical, parse_mode='html')

                markup = InlineKeyboardMarkup(row_width=2)
                markup.add(InlineKeyboardButton('Submit answers', callback_data=f'submit_answers_main_{token_end}'))
                bot.send_message(chat_id, submit_answers, parse_mode='html', reply_markup=markup)

                if excel_test_too_flag == 'Yes':
                    # 30 min before
                    time_left_reminder(call, excel_finish_time_30_min_reminder, token_end, time_left_30_min_message)

                    # 5 min before
                    time_left_reminder(call, excel_finish_time_5_min_reminder, token_end, time_left_5_min_message)

            elif 'submit_answers' in str(call.data):

                candidate_info_dict = process_candidate_temp_info(token_end)
                excel_already_sent = candidate_info_dict['submitted_excel_answer']
                docx_already_sent = candidate_info_dict['submitted_docx_answer']

                if excel_already_sent and docx_already_sent:
                    old_user_handler(chat_id, 'already_processed_users')
                    bot.send_message(chat_id, all_answers_already_submitted)

                else:

                    if 'main' in str(call.data):


                        markup = InlineKeyboardMarkup(row_width=2)

                        if excel_test_too_flag == 'Yes' and not excel_already_sent:
                            markup.add(InlineKeyboardButton('Excel task', callback_data=f'submit_answers_dwnl_excel_{token_end}'))

                        markup.add(InlineKeyboardButton('Clinical part', callback_data=f'submit_answers_dwnl_docx_{token_end}'))

                        bot.send_message(chat_id, choose_answer_section, parse_mode='html', reply_markup=markup)

                    elif 'dwnl' in str(call.data):
                        mode = 'excel' if 'excel' in str(call.data) else 'docx'
                        msg = bot.send_message(chat_id, great_send_file)
                        bot.register_next_step_handler(msg, get_file_msg, token_end, mode)
