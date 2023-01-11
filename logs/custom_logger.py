from datetime import datetime, timedelta
from bot_base.bot_main import *
import os

def log_to_bot_txt(line_to_log):
    with open(os.path.join(os.getcwd(), 'temp_files', 'bot_logs.txt'), 'a') as f:
        f.write(line_to_log)

def logger(message_or_call, error_msg = 'Successful'):
    date = datetime.strftime(datetime.now() + timedelta(hours=8),'%d-%m-%Y:%H-%M')

    first_name = message_or_call.from_user.first_name
    username = message_or_call.from_user.username
    user_id = message_or_call.from_user.id

    try:
        msg_text = message_or_call.text[:65].replace('\n', '. ')
    except:
        try:
            msg_text = message_or_call.data
        except:
            msg_text = 'file'

    status = 'OK' if error_msg == 'Successful' else 'ERROR'

    final_log = f'{status}| {date} | first_name: {first_name} | user_name: {username} | user_id: {user_id} | execution: {error_msg} | msg: {msg_text}'

    print(final_log)

    log_to_bot_txt(f'{final_log}\n')