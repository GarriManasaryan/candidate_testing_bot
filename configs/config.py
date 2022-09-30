import json
from pathlib import Path
from configs.test_conf import *

# You can specify your token here or create a creds_and_tokens.json in home directory
with open (Path.home().joinpath('creds_and_tokens.json')) as f:
    credentials = json.load(f)

TOKEN = credentials.get('telegram_token')
