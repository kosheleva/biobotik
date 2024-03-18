''' Bot tests '''
import unittest
from mocks import AuthMock, StorageAPIClientMock, TGBotMock, TGBotTypesMock, MessageMock, \
    TEST_ROWS_COUNT, TEST_QUESTION_RESPONSE
from src.storage import ExcelStorage
from src.cache import Cache
from src.bot import Bot
from src.texts import ru


class TestBot(unittest.TestCase):
    ''' Bot tests class '''


    @classmethod
    def setUpClass(cls):
        srv_auth = AuthMock()
        srv_api_client = StorageAPIClientMock()

        spreadsheet_id = '123'

        config = {
            "key": "mock_key",
            "path": "mock_path",
            "storage_path": "mock_storage_path"
        }

        storage = ExcelStorage(srv_auth, srv_api_client, spreadsheet_id, config)

        cache = Cache()

        tg_bot = TGBotMock()
        types = TGBotTypesMock()

        cls.bot = Bot(tg_bot, types, storage, cache, ru)

        cls.txt = ru

        cls.message = MessageMock()
        cls.callback_message = MessageMock()


    def test_start(self):
        ''' test for "start" command '''
        result = self.bot.start(self.message)

        self.assertEqual(result['message'], self.txt['welcomeMsg'])
        self.assertEqual(result['chat_id'], 1)


    def test_help(self):
        ''' test for "help" command '''
        result = self.bot.help(self.message)

        expected_msg = f'''
{self.txt["helpMsg"]}
<b>/start</b> {self.txt["helpMsgStart"]}
<b>/help</b> {self.txt["helpMsgHelp"]}
<b>/question_chemistry</b> {self.txt["helpMsgQuestionChemistry"]}
<b>/question_latin</b> {self.txt["helpMsgQuestionLatin"]}
<b>/question_biology</b> {self.txt["helpMsgQuestionBiology"]}
<b>/contacts</b> {self.txt["helpMsgContacts"]}
                '''

        self.assertEqual(result['message'], expected_msg)
        self.assertEqual(result['chat_id'], 1)


    def test_question(self):
        ''' test for "question" command '''
        result = self.bot.question(self.message, 'latin')

        self.assertEqual(
            result['message'],
            f"{TEST_QUESTION_RESPONSE['values'][0][0]}: {TEST_QUESTION_RESPONSE['values'][0][1]}"
        )
        self.assertEqual(result['chat_id'], 1)


    def test_contacts(self):
        ''' test for "contacts" command '''
        test_email = 'email@email.com'
        result = self.bot.contacts(self.message, test_email)

        expected = self.txt['contactsMsg'].replace('{{email}}', test_email)

        self.assertEqual(result['message'], expected)
        self.assertEqual(result['chat_id'], 1)


    def test_show_answer(self):
        ''' test for "show_answer" callback '''
        result = self.bot.show_answer(self.callback_message)

        self.assertEqual(result['message'], TEST_QUESTION_RESPONSE['values'][0][2])
        self.assertEqual(result['chat_id'], 1)


    def test_get_total_rows_count(self):
        ''' test for getting total rows count function '''
        result = self.bot.get_total_rows_count('latin')
        self.assertEqual(result, TEST_ROWS_COUNT)
