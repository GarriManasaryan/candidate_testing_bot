import json
from pathlib import Path
import os

with open (Path.home().joinpath('creds_and_tokens.json')) as f:
    credentials = json.load(f)

# telegram token
TOKEN = credentials.get('telegram_token')

# google service
path_to_google_drive_service_account_json = Path.home().joinpath('google_drive_service.json')

# path to save downloaded files
path_to_download = os.path.join(os.getcwd(), 'downloaded_tasks')

# spreadsheet_with_candidates_info
spreadsheet_id = credentials.get('spreadsheet_id')
sheet_name = credentials.get('sheet_name')
company = credentials.get('company_name')

# spam_defender
with open(os.path.join(os.getcwd(), 'spam_defender', 'banned_list.json')) as f:
    banned_list = json.load(f)

with open(os.path.join(os.getcwd(), 'spam_defender', 'already_processed_users.json')) as f:
    already_processed_users = json.load(f)

# with open(os.path.join(os.getcwd(), 'spam_defender', 'spam_counter.json')) as f:
#     spam_counter = json.load(f)

# message templates
further_instructions_message = 'contact your HR coordinator for further instructions'
welcome_message = f'Welcome to {company} Candidates\' Assessment System! Before we begin, send me your token (candidate_id) like this:\ncand-xx-00000000-xx-0000-000000000000'
verifying_token = f'Verifying token, just a moment'
banned_message = f'Sorry, but you\'ve been banned for spamming; {further_instructions_message}'
invalid_token = f'Invalid token, permission denied; {further_instructions_message}'
file_download = f'Perfect, downloading test files...'
error_downloading_files = f'Something went wrong while donwloading your tasks; {further_instructions_message}'
old_users = f'Your token has been expired; {further_instructions_message}'

# instructions
excel_time_limit = 4
time_difference = 8
timedelta_time_left_30_min = excel_time_limit - 0.5 + time_difference
timedelta_time_left_5_min = excel_time_limit - 0.08 + time_difference

instruction_start = 'Instructions:'
instruction_time_limit_excel = f'Time limit: <b>{str(excel_time_limit)} hours</b>'
instruction_time_limit_clinical = 'Time limit: <b>1 week</b> (approximately)'
sep_file_instr = 'If you have several files, you need to click "Submit answers" for every file separately and send them one by one'

instruction_clinical_part = f'• <u>Clinical part</u>: theoretical questions in a cancer-specific field.\n{instruction_time_limit_excel}'
instruction_excel = f'• <u>Excel basics</u>: you will be given an excel file with a series of practice tasks. For example, calculate duplicated values in the table or filter data using formulas etc.\n{instruction_time_limit_clinical}'
instruction_sending_answers = f'<i>How to send back files with answers?</i>\n\nA message will be sent to you with a button "Submit answers": click it, choose task and send the file. {sep_file_instr}. Make sure, you get the response from bot (successfully submitted)'
instruction_all_answers = 'All answers should be submitted in the same file and sent back to this bot'
instruction_end = 'When you are ready, click "Start". Best of luck :)'

full_task_instr = '\n\n'.join([instruction_start, instruction_clinical_part, instruction_excel, instruction_sending_answers])
just_clinical_task_instr = '\n\n'.join([instruction_start, instruction_clinical_part, instruction_sending_answers])
just_excel_instr = '\n\n'.join([instruction_start, instruction_excel, instruction_sending_answers])

# answers
submit_answers = f'When you are done, press "Submit answers". {sep_file_instr}'
choose_answer_section = 'Which task?'
great_send_file = 'Great! Send the file'
success_answer_saved = 'Successfully saved the answer!'
all_answers_already_submitted = 'You have already submitted all answers'

# reminders
time_left_base_message = 'Warning! You have less than <b>TIME_LEFT minutes</b> to submit an excel task'
time_left_30_min_message = time_left_base_message.replace('TIME_LEFT', '30')
time_left_5_min_message = time_left_base_message.replace('TIME_LEFT', '5')

# customs
start_already_pushed = 'Your test has already started, use the buttons above to submit answers'
answer_already_provided = 'Your answer for this task has been already accepted'
both_answers_have_been_submitted = all_answers_already_submitted

# rules
rules_and_warnings = 'Important rules:\n\n1. All answers should be submitted in the same file and sent back to this bot\n\n2. Don\'t change the format of sent files.\n\n3. Don\'t rename sent files: as mentioned before, just submit your answers and send them back in the same file.\n\n4. You can submit the answer files only once, so be careful'
