from bot_base.bot_main import *
from telegram_handlers.error_handlers import *
from services.google_service import *
from time import sleep
from datetime import datetime, timedelta
from bot_reboot.ressurection_handler import *

# connect to drive and google_sheets
gsr = GoogleServiceHandler()

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

        if text == '/start':
            if user_is_spamming(message, chat_id):
                bot.send_message(chat_id, banned_message)

            else:
                msg = bot.send_message(chat_id, welcome_message)
                bot.register_next_step_handler(msg, process_token_from_candidate)

@message_error_handler()
def user_is_spamming(message, chat_id):
    chat_id_string = str(chat_id)

    if chat_id_string != developer_chat_id:
        with open(os.path.join(os.getcwd(), 'spam_defender_files', 'spam_counter.json')) as f:
            spam_counter = json.load(f)

        clicked = spam_counter.get(chat_id_string, 0)
        spam_counter[chat_id_string] = clicked + 1

        with open(os.path.join(os.getcwd(), 'spam_defender_files', 'spam_counter.json'), 'w') as f:
            json.dump(spam_counter, f)

        if spam_counter.get(chat_id_string) > 3:
            old_user_handler(chat_id, 'banned_list')
            return True

        else:
            return False

    else:
        return False

def old_user_handler(user_chat_id, old_user_reason_list):
    with open(os.path.join(os.getcwd(), 'spam_defender_files', f'{old_user_reason_list}.json'), 'w') as f:
        source_list = banned_list if old_user_reason_list == 'banned_list' else already_processed_users
        source_list.append(user_chat_id)
        json.dump(source_list, f)

@message_error_handler()
def process_token_from_candidate(message):
    token = message.text
    chat_id = message.chat.id

    bot.send_message(chat_id, verifying_token)
    sleep(1)

    df_all_candidates, worksheet = gsr.get_google_sheet_df()
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
                bot.send_message(chat_id, full_task_instr, parse_mode='html')

            else:
                bot.send_message(chat_id, just_clinical_task_instr, parse_mode='html')

            bot.send_message(chat_id, rules_and_warnings, parse_mode='html')
            bot.send_message(chat_id, instruction_end, parse_mode='html', reply_markup=markup)

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

def check_if_both_tasks_are_finished(token_end):
    candidate_info_dict = process_candidate_temp_info(token_end)
    excel_already_sent = candidate_info_dict['submitted_excel_answer']
    docx_already_sent = candidate_info_dict['submitted_docx_answer']

    condition_to_check = excel_already_sent and docx_already_sent

    return condition_to_check, candidate_info_dict

def upload_results_to_google_sheet(token_end):
    try:
        # in prev step is updated → refresh
        candidate_info_dict = process_candidate_temp_info(token_end)
        token = candidate_info_dict.get('token')

        df_all_candidates, worksheet = gsr.get_google_sheet_df()
        df_all_candidates = df_all_candidates.reset_index(drop=True)
        df_candidate_filter = df_all_candidates[df_all_candidates['token']==token]

        for i, row in df_candidate_filter.iterrows():
            df_candidate_filter.loc[i, 'Start_time'] = candidate_info_dict.get('Start_time')
            df_candidate_filter.loc[i, 'End_time'] = candidate_info_dict.get('End_time')
            df_candidate_filter.loc[i, 'Time_spent'] = candidate_info_dict.get('Time_spent')
            df_candidate_filter.loc[i, 'Finished_in_time'] = candidate_info_dict.get('Finished_in_time')
            df_candidate_filter.loc[i, 'Link_to_candidate_google_folder'] = candidate_info_dict.get('Link_to_candidate_google_folder')

        row_index = list(df_candidate_filter.index)[0]
        new_row = list(df_candidate_filter.loc[row_index])

        gsr.update_row(worksheet, new_row, row_index + 2)

    except Exception as e:
        print(repr(e))

def upload_to_google_folder(token_end, candidate_info_dict):

    # create candidate folder in google drive
    team_parent_folder_id = credentials['teams'][candidate_info_dict['CIT_department']]
    folder_name = candidate_info_dict['Last_name'] + '_' + candidate_info_dict['First_name']
    res_candidate_folder_id = gsr.create_google_folder(team_parent_folder_id, folder_name).get('id')
    candidate_info_dict['Link_to_candidate_google_folder'] = f'https://drive.google.com/drive/u/0/folders/{res_candidate_folder_id}'

    process_candidate_temp_info(token_end, 'save_dict', candidate_info_dict)

    # upload files
    for key, value in candidate_info_dict.items():
        if 'file_name' in key:
            file_name = value
            file_full_path = os.path.join(os.getcwd(), 'downloaded_tasks', file_name)
            mimetype = key.split('_')[0]

            sleep(5)
            gsr.add_file_to_google_folder(res_candidate_folder_id, file_name, file_full_path, mimetype)

def sent_answer_files_are_in_correct_format(message, mode):
    file_format = message.document.file_name.split('.')[-1]

    if (mode == 'excel' and file_format == 'xlsx') or (mode == 'docx' and file_format == 'docx'):
        return True

def google_logger(msg_text):
    print(msg_text)
    with open(os.path.join(os.getcwd(), 'temp_files', 'bot_logs.txt'), 'a') as f:
        f.write(f'{msg_text}\n')

@message_error_handler()
def get_file_msg(message, token_end, mode):

    if sent_answer_files_are_in_correct_format(message, mode):
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

        # if completed, create google folder per candidate and fill google sheet with time results
        both_tasks_are_finished, candidate_info_dict = check_if_both_tasks_are_finished(token_end)

        if both_tasks_are_finished:
            # create google folder with candidate's answer
            upload_to_google_folder(token_end, candidate_info_dict)
            google_logger('-> Saved files to google drive')

            # update google sheets
            upload_results_to_google_sheet(token_end)
            google_logger('-> Filled results in google sheets')

            # email notification to manager
            destination_email = candidate_info_dict['CIT_team_lead_email']
            subject = f'Candidate {last_name} {first_name} finished the test'
            link_to_main_google = f'https://docs.google.com/spreadsheets/d/{spreadsheet_id}'
            body = f'Link to candidate\'s results:\n\n{link_to_main_google}'

            gsr.send_email_confirmation(destination_email, subject, body)
            google_logger('-> Sent a confirmation email')

    else:
        bot.send_message(message.chat.id, wrong_answer_file_format)

def calculate_spent_time(token_end):
    candidate_info_dict = process_candidate_temp_info(token_end)
    candidate_info_dict['End_time'] = datetime.strftime(datetime.now(),'%H:%M - %d.%m.%Y')

    time_spent = round((datetime.strptime(candidate_info_dict['End_time'], '%H:%M - %d.%m.%Y') - datetime.strptime(candidate_info_dict['Start_time'], '%H:%M - %d.%m.%Y')).total_seconds()/60/60, 2)

    candidate_info_dict['Time_spent'] = time_spent
    candidate_info_dict['Finished_in_time'] = time_spent < 4

    process_candidate_temp_info(token_end, 'save_dict', candidate_info_dict)

@bot.callback_query_handler(func=lambda call: True)
@message_error_handler()
def callback_handler(call):

    if call.message:
        chat_id = call.message.chat.id

        if chat_id in already_processed_users or chat_id in banned_list:
            bot.send_message(chat_id, old_users)

        else:
            token_end = str(call.data).split('_')[-1]

            both_tasks_are_finished, candidate_info_dict = check_if_both_tasks_are_finished(token_end)

            excel_test_too_flag = candidate_info_dict.get('Send_excel_test_too')

            if 'start_the_test' in str(call.data):

                if both_tasks_are_finished:
                    bot.send_message(chat_id, both_answers_have_been_submitted)

                elif candidate_info_dict['Start_time'] != '':
                    bot.send_message(chat_id, start_already_pushed)

                else:

                    candidate_info_dict['Start_time'] = datetime.strftime(datetime.now(),'%H:%M - %d.%m.%Y')

                    process_candidate_temp_info(token_end, 'save_dict', candidate_info_dict)

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

                excel_already_sent = candidate_info_dict['submitted_excel_answer']
                docx_already_sent = candidate_info_dict['submitted_docx_answer']

                if excel_already_sent and docx_already_sent:
                    old_user_handler(chat_id, 'already_processed_users')
                    bot.send_message(chat_id, all_answers_already_submitted)

                else:

                    if 'main' in str(call.data):

                        markup = InlineKeyboardMarkup(row_width=2)

                        if not excel_already_sent and not docx_already_sent:

                            if excel_test_too_flag == 'Yes':
                                markup.add(InlineKeyboardButton('Excel task', callback_data=f'submit_answers_dwnl_excel_{token_end}'))

                            markup.add(InlineKeyboardButton('Clinical part', callback_data=f'submit_answers_dwnl_docx_{token_end}'))
                            bot.send_message(chat_id, choose_answer_section, parse_mode='html', reply_markup=markup)

                        elif excel_already_sent and not docx_already_sent:
                            markup.add(InlineKeyboardButton('Clinical part', callback_data=f'submit_answers_dwnl_docx_{token_end}'))
                            bot.send_message(chat_id, choose_answer_section, parse_mode='html', reply_markup=markup)

                        elif not excel_already_sent and docx_already_sent:
                            markup.add(InlineKeyboardButton('Excel task', callback_data=f'submit_answers_dwnl_excel_{token_end}'))
                            bot.send_message(chat_id, choose_answer_section, parse_mode='html', reply_markup=markup)

                        else:
                            bot.send_message(chat_id, answer_already_provided)

                    elif 'dwnl' in str(call.data):
                        mode = 'excel' if 'excel' in str(call.data) else 'docx'

                        if (docx_already_sent and mode == 'docx') or (excel_already_sent and mode == 'excel'):
                            bot.send_message(chat_id, answer_already_provided)

                        else:

                            if mode == 'excel':
                                calculate_spent_time(token_end)

                            msg = bot.send_message(chat_id, great_send_file)
                            bot.register_next_step_handler(msg, get_file_msg, token_end, mode)
