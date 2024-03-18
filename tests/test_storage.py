''' Tests for storage '''
import unittest
from mocks import AuthMock, StorageAPIClientMock, TEST_ROWS_COUNT, \
    TEST_QUESTION_NUMBER, TEST_QUESTION_RESPONSE, SPREADSHEET_ID, CONFIG
from src.storage import ExcelStorage


class TestStorage(unittest.TestCase):
    ''' Storage tests '''


    @classmethod
    def setUpClass(cls):
        # pylint: disable=duplicate-code
        srv_auth = AuthMock()
        srv_api_client = StorageAPIClientMock()

        spreadsheet_id = SPREADSHEET_ID

        config = CONFIG

        cls.storage = ExcelStorage(srv_auth, srv_api_client, spreadsheet_id, config)


    def test_authorize(self):
        ''' test for authorization '''
        srv_storage = self.storage.authorize()
        self.assertIsInstance(srv_storage, StorageAPIClientMock)


    def test_get_total_rows_count(self):
        ''' test for getting total rows count '''
        result = self.storage.get_total_rows_count('latin')
        self.assertEqual(result, TEST_ROWS_COUNT)


    def test_get_question(self):
        ''' test for getting question '''

        result = self.storage.get_question('latin', TEST_QUESTION_NUMBER)

        expected_result = {
            "category": TEST_QUESTION_RESPONSE["values"][0][0],
            "question": TEST_QUESTION_RESPONSE["values"][0][1],
            "question_image": '',
            "answer": TEST_QUESTION_RESPONSE["values"][0][2],
            "answer_image": '',

        }
        self.assertDictEqual(result, expected_result)
