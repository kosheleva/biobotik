''' Bot tests: error cases '''
import unittest
from mocks import AuthMock, StorageAPIClientErrorMock, TGBotMock, TGBotTypesMock, MessageMock, \
    SPREADSHEET_ID, CONFIG
from src.storage import ExcelStorage
from src.cache import Cache
from src.bot import Bot
from src.texts import ru


class TestBotErrors(unittest.TestCase):
    ''' Bot errors tests '''

    @classmethod
    def setUpClass(cls):
        srv_auth = AuthMock()
        srv_api_client_error = StorageAPIClientErrorMock()

        spreadsheet_id = SPREADSHEET_ID

        config = CONFIG

        storage_error = ExcelStorage(srv_auth, srv_api_client_error, spreadsheet_id, config)

        cache = Cache()

        tg_bot = TGBotMock()
        types = TGBotTypesMock()

        cls.bot_with_storage_error = Bot(tg_bot, types, storage_error, cache, ru)

        cls.txt = ru

        cls.message = MessageMock()


    def test_question(self):
        ''' error test case on question request '''
        result = self.bot_with_storage_error.question(self.message, 'latin')
        self.assertEqual(result['message'], self.txt['serviceErrorMsg'])
