''' Storage module '''
import logging
from abc import ABC, abstractmethod
from utils.retry import retry


class Storage(ABC):
    ''' Storage interface '''

    @abstractmethod
    def authorize(self):
        ''' authorization '''


    @abstractmethod
    def get_total_rows_count(self, sheet):
        ''' get count of rows in storage '''


    @abstractmethod
    def get_question(self, sheet, number):
        ''' get question data from storage '''



class ExcelStorage(Storage):
    ''' Excel storage class '''


    def __init__(self, auth_srv, api_client, spreadsheet_id, config):
        self.auth = auth_srv
        self.api_client = api_client
        self.spreadsheet_id = spreadsheet_id
        self.config = config

        self.authorize()


    @retry(max_retries=2, wait_time=1)
    def authorize(self):
        ''' authorize account in storage '''

        logging.info('Storage authorization requested.')

        http_auth = self.auth.authorize_from_json(
            self.config['key'],
            self.config['path'],
            self.config['storage_path']
        )
        self.service = self.api_client.build('sheets', 'v4', http = http_auth)
        return self.service


    @retry(max_retries=2, wait_time=1)
    def get_total_rows_count(self, sheet):
        res = self.service.spreadsheets().get(spreadsheetId=self.spreadsheet_id).execute()

        for item in res['sheets']:
            if item['properties']['title'] == sheet:
                return item['properties']['gridProperties']['rowCount']

        return 0


    @retry(max_retries=2, wait_time=1)
    def get_question(self, sheet, number):
        response = self.service.spreadsheets().values().get(
                spreadsheetId = self.spreadsheet_id,
                range = f'''{sheet}!A{number}:C{number}''',
                majorDimension = 'ROWS'
            ).execute()

        question_data = response['values'][0][1].split(';')
        if len(question_data) == 1:
            question_data.append('')

        answer_data = response['values'][0][2].split(';')
        if len(answer_data) == 1:
            answer_data.append('')

        return {
            'category': response['values'][0][0],
            'question': question_data[0].strip(),
            'question_image': question_data[1].strip(),
            'answer': answer_data[0].strip(),
            'answer_image': answer_data[1].strip()
        }
