''' Storage api client wrapper '''

from apiclient import discovery

class StorageApiClient():
    ''' API client class '''


    def build(self, sheets, v, http):
        ''' Build storage service '''
        return discovery.build(sheets, v, http = http)
