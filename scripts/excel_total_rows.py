''' Script to get total rows of excel sheet '''

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


# GET ROWS COUNT
# pylint: disable=no-member
res = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()

for item in res['sheets']:
    print(item['properties']['title'])
    print(item['properties']['gridProperties']['rowCount'])

totalRowsCount = res['sheets'][0]['properties']['gridProperties']['rowCount']


print(totalRowsCount)
