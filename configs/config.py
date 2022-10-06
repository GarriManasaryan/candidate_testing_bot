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

# message templates
further_instructions_message = 'contact your HR coordinator for further instructions'
welcome_message = f'Welcome to {company} Candidates\' Assessment System! Before we begin, send me your token (candidate_id) like this:\ncand-xx-00000000-xx-0000-000000000000'
verifying_token = f'Verifying token, just a moment'
banned_message = f'Sorry, but you\'ve been banned for spamming; {further_instructions_message}'
invalid_token = f'Invalid token, permission denied; {further_instructions_message}'
file_download = f'Perfect, downloading test files...'
error_downloading_files = f'Something went wrong while donwloading your tasks; {further_instructions_message}'
old_users = f'Your token has been expired; {further_instructions_message}'
