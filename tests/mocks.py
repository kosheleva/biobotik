''' Test mocks implementation '''
TEST_ROWS_COUNT = 10
TEST_QUESTION_NUMBER = 1
TEST_QUESTION_RESPONSE = {
    'range': 'latin!A3:C3', 
    'majorDimension': 'ROWS', 
    'values': [['Grammar', 'Question1', 'Answer1']]
}

SPREADSHEET_ID = '123'

CONFIG = {
    "key": "mock_key",
    "path": "mock_path",
    "storage_path": "mock_storage_path"
}


class AuthMock():
    ''' Auth mock class '''

    # pylint: disable=unused-argument
    def authorize_from_json(self, json, service_path, storage_path):
        ''' mock method implementation '''
        return True


class AuthErrorMock():
    ''' Auth error mock class '''


    def authorize_from_json(self, json, service_path, storage_path):
        ''' mock method with error implementation '''
        raise Exception('''HttpAccessTokenRefreshError.
                        Invalid OAuth scope or ID token audience provided.''')



class StorageAPIClientMock():
    ''' Storage api client mock class '''


    def __init__(self):
        self.is_values = False

    # pylint: disable=unused-argument
    def build(self, sheets, version, http):
        ''' mock method implementation'''
        return self


    def spreadsheets(self):
        ''' mock method implementation'''
        return self

    # pylint:disable=invalid-name, unused-argument, redefined-builtin
    def get(self, spreadsheetId, range=None, majorDimension=None):
        ''' mock method implementation'''
        return self


    def execute(self):
        ''' mock method implementation'''
        response = None

        if not self.is_values:
            response = {
                "sheets": [
                    {
                        "properties": {
                            "title": "latin",
                            "gridProperties": { "rowCount": TEST_ROWS_COUNT }
                        }
                    }
                ] }
        else:
            response = TEST_QUESTION_RESPONSE

        self.is_values = False

        return response


    def values(self):
        ''' mock method implementation'''
        self.is_values = True
        return self


class StorageAPIClientErrorMock():
    ''' Storage api client error mock class '''

    # pylint:disable=unused-argument
    def build(self, sheets, version, http):
        ''' mock method implementation'''
        return self


    def spreadsheets(self):
        ''' mock method implementation'''
        raise Exception("Service unavailable.")


class TGBotTypesMock():
    ''' Telegram bot types mock class '''

    # disable PascalCase as it is bot library methods naming
    # pylint: disable=invalid-name, unused-argument
    def ReplyKeyboardMarkup(self, row_width=None, resize_keyboard=False):
        ''' mock method implementation'''
        return self


    def add(self, *args):
        ''' mock method implementation'''
        return self


    def KeyboardButton(self, arg):
        ''' mock method implementation'''
        return self


    def InlineKeyboardMarkup(self, row_width=None):
        ''' mock method implementation'''
        return self


    def InlineKeyboardButton(self, text="test", callback_data="test"):
        ''' mock method implementation'''
        return self


class TGBotMock():
    ''' Telegram bot mock class '''

    # pylint: disable=unused-argument
    def send_message(self, chat_id, msg, reply_markup=None, parse_mode='html'):
        ''' mock method implementation'''
        result = {
            "chat_id": chat_id,
            "message": msg
        }
        return result


    def send_photo(self, chat_id, photo=None, caption=None, reply_markup = None):
        ''' mock method implementation'''
        result = {
            "chat_id": chat_id,
            "message": caption
        }
        return result


class ChatMock():
    ''' Message chat object mock class '''
    id = 1


class MessageMock():
    ''' Message object mock class '''

    chat = ChatMock()

    data = f"show_answer_{chat.id}_latin_{TEST_QUESTION_NUMBER}"
