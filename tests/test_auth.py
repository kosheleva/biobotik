''' Auth tests '''
import unittest
from unittest.mock import patch, MagicMock
from src.auth import OAuth


class TestAuth(unittest.TestCase):
    ''' Auth tests class '''


    def setUp(self):
        self.srv_auth = OAuth()


    @patch('src.auth.ServiceAccountCredentials')
    def test_authorize_from_json_success(self, mock_srv_acc_credentials):
        ''' success authorization case '''
        mock_srv_acc_credentials.return_value = {}

        http_auth = self.srv_auth.authorize_from_json({}, '', '')
        self.assertIsInstance(http_auth, MagicMock)


    @patch('src.auth.ServiceAccountCredentials.from_json_keyfile_dict')
    def test_authorize_from_json_error(self, mock_srv_acc_credentials):
        ''' error authorization case '''
        mock_srv_acc_credentials.side_effect = Exception()

        http_auth = self.srv_auth.authorize_from_json({}, '', '')
        self.assertIsNone(http_auth)
