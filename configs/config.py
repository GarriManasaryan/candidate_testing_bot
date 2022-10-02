import json
from pathlib import Path
import os

# You can specify your token here or create a creds_and_tokens.json in home directory
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
