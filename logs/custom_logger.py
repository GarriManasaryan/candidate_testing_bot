from datetime import datetime, timedelta
from bot_base.bot_main import *
import traceback

def logger(message_or_call, error_msg = 'Successful'):
    date = datetime.strftime(datetime.now() + timedelta(hours=8),'%d-%m-%Y:%H-%M')

    first_name = message_or_call.from_user.first_name
    username = message_or_call.from_user.username
    user_id = message_or_call.from_user.id

    try:
        msg_text = message_or_call.text[:65].replace('\n', '. ')
    except:
        msg_text = message_or_call.data

    status = 'OK' if error_msg == 'Successful' else 'ERROR'

    print(f'{status}| {date} | first_name: {first_name} | username: {username} | user_id: {user_id} | execution: {error_msg} | msg: {msg_text}')

# def traceback_log(message_or_call, module):
#
#     try:
#         user_chat_id = message_or_call.from_user.id
#     except:
#         user_chat_id = message_or_call.chat.id
#
#     with open(os.path.join(logs_folder, f'BOB_errors_{user_chat_id}_{module}.txt'), 'w') as f:
#         f.write(traceback.format_exc())
