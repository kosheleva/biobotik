''' Script to get excel data '''

from os import getenv
import json
import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv

# pylint: disable=duplicate-code
load_dotenv()


# AUTH
credentials = json.loads(getenv('EXCEL_KEY'))
excel_path = getenv('EXCEL_PATH')
storage_path = getenv('EXCEL_STORAGE_PATH')
spreadsheet_id = getenv('SPREADSHEET_ID')

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


# GET VALUES
# pylint: disable=no-member
values = service.spreadsheets().values().get(
    spreadsheetId = spreadsheet_id,
    range = 'chemistry!A1:C1',
    majorDimension = 'ROWS'
).execute()

print(values)
