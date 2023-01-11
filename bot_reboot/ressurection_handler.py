from time import sleep
import os
from logs.custom_logger import *

def bot_priest():

    def bot_priest_wrapper(func):

        def wrapper_func(*args, **kwargs):

            while True:

                try:
                    func(*args, **kwargs)

                except Exception as e:
                    print('\n---Oups! It seems i\'ve just died... for some reason. Rebooting in 60 seconds---\n')

                    print(f'Detailed error: {repr(e)}')
                    # with open(os.path.join(os.getcwd(), 'temp_files', 'bot_logs.txt'), 'a') as f:
                    #     f.write(f'\n{repr(e)}\n')

                    log_to_bot_txt(f'\n{repr(e)}\n')

                    sleep(60)
                    print('\n---Successfully resurrected myself---\n')

        return wrapper_func

    return bot_priest_wrapper
