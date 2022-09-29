import json
from pathlib import Path

# You can specify your token here or create a creds_and_tokens.json in home directory
with open (Path.home().joinpath('creds_and_tokens.json')) as f:
    credentials = json.load(f)

with open('test.json') as f:
    test_json = json.load(f)

TOKEN = credentials.get('telegram_token')
