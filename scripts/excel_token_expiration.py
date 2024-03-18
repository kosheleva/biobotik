''' Script to check token expiration '''

from os import getenv
import json
import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv


load_dotenv()


# AUTH
credentials = json.loads(getenv('EXCEL_KEY'))
excel_path = getenv('EXCEL_PATH')
storage_path = getenv('EXCEL_STORAGE_PATH')
spreadsheet_id = getenv('SPREADSHEET_ID')

# pylint: disable=duplicate-code
credentials = ServiceAccountCredentials.from_json_keyfile_dict(
    credentials,
    [
        excel_path,
        storage_path
    ]
)
httpAuth = credentials.authorize(httplib2.Http())

# GET SERVICE
service = apiclient.discovery.build('sheets', 'v4', http = httpAuth)

while True:
    command = input("> ").lower()

    if command == 'check':
        try:
            # pylint: disable=no-member
            values = service.spreadsheets().values().get(
                spreadsheetId = spreadsheet_id,
                range = 'chemistry!A3:C3',
                majorDimension = 'ROWS'
            ).execute()

            print('---All good---')
            print(values)
            print(credentials.get_access_token())
        except Exception as e:
            print('---Exception---')
            print(e)
            print(credentials.get_access_token())
    elif command == 'q':
        break
    else:
        print('Command not found')
