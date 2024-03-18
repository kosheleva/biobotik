''' Auth module '''
import logging
from abc import ABC, abstractmethod
from oauth2client.service_account import ServiceAccountCredentials
import httplib2


class Auth(ABC):
    ''' Auth class interface '''


    @abstractmethod
    def authorize_from_json(self, json, service_path, storage_path):
        ''' authorization from file '''


class OAuth(Auth):
    ''' OAuth class '''


    def authorize_from_json(self, json, service_path, storage_path):
        ''' authorization from file '''
        try:
            # Returns:
            # ValueError, if the credential type is not SERVICE_ACCOUNT;
            # KeyError, if one of the expected keys is not present in the keyfile.
            credentials = ServiceAccountCredentials.from_json_keyfile_dict(
                        json,
                        [ service_path, storage_path ]
                    )

            http_auth = credentials.authorize(httplib2.Http())
        except Exception as e:
            logging.exception(e)
            return None
        else:
            return http_auth
        finally:
            logging.info('Authorization is finished.')
