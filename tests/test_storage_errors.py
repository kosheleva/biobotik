''' Tests for storage errors '''
import unittest
from mocks import AuthMock, AuthErrorMock, StorageAPIClientMock, StorageAPIClientErrorMock, \
    TEST_QUESTION_NUMBER, SPREADSHEET_ID, CONFIG
from src.storage import ExcelStorage


class TestStorageErrors(unittest.TestCase):
    ''' Storage error test cases '''


    @classmethod
    def setUpClass(cls):
        # pylint: disable=duplicate-code
        srv_auth = AuthMock()
        srv_api_client = StorageAPIClientMock()

        spreadsheet_id = SPREADSHEET_ID

        config = CONFIG

        cls.storage = ExcelStorage(srv_auth, srv_api_client, spreadsheet_id, config)


    def test_authorize_error(self):
        ''' test for authorization error '''
        srv_auth = AuthErrorMock()
        srv_api_client = StorageAPIClientMock()

        spreadsheet_id = SPREADSHEET_ID

        config = CONFIG

        with self.assertRaises(Exception):
            self.storage = ExcelStorage(srv_auth, srv_api_client, spreadsheet_id, config)


    def test_get_total_rows_count_error(self):
        ''' test for storage error on getting total count of rows '''
        srv_auth = AuthMock()
        srv_api_client = StorageAPIClientErrorMock()

        spreadsheet_id = SPREADSHEET_ID

        config = CONFIG

        self.storage = ExcelStorage(srv_auth, srv_api_client, spreadsheet_id, config)

        with self.assertRaises(Exception):
            self.storage.get_total_rows_count('latin')


    def test_get_question(self):
        ''' test for storage error on getting question '''
        srv_auth = AuthMock()
        srv_api_client = StorageAPIClientErrorMock()

        spreadsheet_id = SPREADSHEET_ID

        config = CONFIG

        self.storage = ExcelStorage(srv_auth, srv_api_client, spreadsheet_id, config)

        with self.assertRaises(Exception):
            self.storage.get_question('latin', TEST_QUESTION_NUMBER)
