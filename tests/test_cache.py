''' Cache tests '''
import unittest
from src.cache import Cache


class TestCache(unittest.TestCase):
    ''' Class for cache testing '''


    def setUp(self):
        self.cache = Cache()


    def test_set(self):
        ''' test for setting a cache value '''
        key = '2024-01-01'
        value = 1000
        result = self.cache.set(key, value)

        self.assertEqual(result, value)


    def test_get_non_exist_key(self):
        ''' test for getting non existing key '''
        key = 'non-exist-key'
        get_result = self.cache.get(key)

        self.assertIsNone(get_result)


    def test_get(self):
        ''' test for getting a value from cache '''
        key = '2024-01-01'
        value = 1000
        set_result = self.cache.set(key, value)

        self.assertEqual(set_result, value)

        get_result = self.cache.get(key)

        self.assertEqual(get_result, value)


    def test_clear(self):
        ''' test for clearing a cache '''
        key = '2024-01-01'
        value = 1000
        set_result = self.cache.set(key, value)

        self.assertEqual(set_result, value)

        get_result = self.cache.get(key)

        self.assertEqual(get_result, value)

        self.cache.clear()

        clear_result = self.cache.get(key)

        self.assertIsNone(clear_result)
