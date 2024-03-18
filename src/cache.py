''' Cache implementation '''

import logging

class Cache:
    ''' Cache class'''


    def __init__(self):
        self.cache = {}


    def clear(self):
        ''' clear value from cache '''
        self.cache = {}


    def get(self, key):
        ''' get value from cache '''

        logging.info(self.cache)

        try:
            return self.cache[key]
        except Exception:
            logging.warning('No such key in storage: %s', key)
            return None


    def set(self, key, value):
        ''' set value in cache '''
        self.cache[key] = value
        return self.cache[key]
