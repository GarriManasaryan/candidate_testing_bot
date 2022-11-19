from time import sleep

def bot_priest():

    def bot_priest_wrapper(func):

        def wrapper_func(*args, **kwargs):

            while True:

                try:
                    func(*args, **kwargs)

                except Exception as e:
                    print('\n---Oups! It seems i\'ve just died... for some reason. Rebooting in 60 seconds---\n')
                    print(f'Detailed error: {repr(e)}')
                    sleep(60)
                    print('\n---Successfully resurrected myself---\n')

        return wrapper_func

    return bot_priest_wrapper
