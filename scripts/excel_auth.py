''' Script to run authorization for excel '''

from os import getenv
import json
import httplib2
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv


load_dotenv()

# AUTH
credentials = json.loads(getenv('EXCEL_KEY'))
excel_path = getenv('EXCEL_PATH')
storage_path = getenv('EXCEL_STORAGE_PATH')

# pylint: disable=duplicate-code
credentials = ServiceAccountCredentials.from_json_keyfile_dict(
    credentials,
    [
        excel_path,
        storage_path
    ]
)

httpAuth = credentials.authorize(httplib2.Http())

print('MAX_TOKEN_LIFETIME_SECS', credentials.MAX_TOKEN_LIFETIME_SECS)
print(credentials.get_access_token())
