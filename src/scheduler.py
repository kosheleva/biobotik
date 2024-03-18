''' Scheduler module '''
import logging
from threading import Timer


class Scheduler:
    ''' Class to run specific tasks by schedule '''
    def __init__(self, cache, config):
        self.cache = cache
        self.config = config

        self.timer = None

        logging.info('Scheduler is initialized.')


    def clear_cache_task(self):
        ''' Clear cache task'''
        self.cache.clear()


    def clear_file_task(self):
        ''' Clear file task '''
        open(self.config['log_filename'], 'w', encoding='utf-8').close()


    def cancel(self):
        ''' Stop the timer '''
        self.timer.cancel()


    def callback(self):
        ''' Timer callback '''

        self.clear_cache_task()
        self.clear_file_task()

        self.run()


    def run(self):
        ''' Schedule tasks '''
        try:
            logging.info('Scheduler start running tasks.')

            self.timer = Timer(self.config['scheduler_time'], self.callback)
            self.timer.start()
        except Exception as e:
            logging.exception(e)
        finally:
            logging.info('Scheduler tasks are done.')
