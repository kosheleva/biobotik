''' Utils tests '''
import unittest
import datetime
import utils


class TestUtils(unittest.TestCase):
    ''' Class for utils tests'''


    def test_get_random_number(self):
        ''' test cases for getting random number '''

        # normal case
        x1 = utils.get_random_number(1, 5, 1)
        self.assertIn(x1, [1, 2, 3, 4, 5])

        # start value > end value
        x2 = utils.get_random_number(5, 1, 1)
        self.assertIn(x2, [1, 2, 3, 4, 5])

        # step > end - start
        x3 = utils.get_random_number(1, 5, 20)
        self.assertEqual(x3, 1)

        # range contains one number
        x4 = utils.get_random_number(1, 1, 1)
        self.assertEqual(x4, 1)

        # negative numbers
        x5 = utils.get_random_number(-1, -5, 1)
        self.assertIn(x5, [-1, -2, -3, -4, -5])


    def test_get_current_date(self):
        ''' test case for getting current date '''
        date = utils.get_current_date()

        self.assertIsNotNone(date)
        self.assertIsInstance(date, datetime.date)
        self.assertEqual(date, datetime.date.today())
