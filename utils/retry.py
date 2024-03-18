''' Retry utils '''
import time
import logging

def retry(max_retries, wait_time):
    ''' Implementation of retry mechanism'''
    def decorator(func):
        def wrapper(*args, **kwargs):
            retries = 0
            while retries < max_retries:
                try:
                    result = func(*args, **kwargs)
                    return result
                except Exception as e:
                    logging.error(e)
                    retries += 1
                    time.sleep(wait_time)

            logging.critical('Max retries of function %s exceeded.', func)

            raise Exception(f'Max retries of function {func} exceeded')
        return wrapper
    return decorator
