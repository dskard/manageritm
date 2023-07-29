import textwrap
import requests

from manageritm.client.manageritm_client import ManagerITMClient


class ManagerITMProxyClient(ManagerITMClient):
    def __init__(self, manageritm_uri):
        super().__init__(manageritm_uri)

    def client(self, port=None, webport=None, har=None):
        data = {
            'port': port,
            'webport': webport,
            'har': har,
        }

        result = self._http(requests.post, "/client/proxy", json=data)
        self._client_id = result["client_id"]
        return result
