import textwrap
import requests


class ManagerITMClientException(Exception):
    def __init__(self, response):
        self.response = response

    def __repr__(self):
        return f"<{self.__class__.__name__} status={self.response.status_code}>"

    def __str__(self):
        req = self.response.request
        return textwrap.dedent(
            f"""
            Failed to execute {self.__class__.__name__} request:
            \t{req.method} {req.url}
            Body:
            \t{req.body}
            Response status code:
            \t{self.response.status_code}
            Response body:
            \t{self.response.text}
            """
        ).strip()


class ManagerITMClient:
    def __init__(self, mitmmanager_uri):
        self._uri = mitmmanager_uri
        self._client_id = None

    def __del__(self):
        if self._client_id is not None:
            status = self.proxy_status()["status"]
            # status  |  meaning
            # --------+-------------------------------
            # None    |  process still running
            # -1      |  process exited with error
            #  0      |  process exited successfully
            #  1      |  process error while starting
            if status not in [None, -1, 0, 1]:
                self.proxy_stop()
                self._client_id = None

    def _check_status(self, response):
        if response.status_code >= 400:
            raise ManagerITMClientException(response)

    def _http(self, method, uri, **kwargs):
        endpoint = self._uri + uri
        r = method(endpoint, **kwargs)
        self._check_status(r)

        return r.json()

    def client(self, port=None, webport=None):
        params = {}
        if port is not None:
            params['port'] = port
        if webport is not None:
            params['webport'] = webport

        result = self._http(requests.get, "/client", params=params)
        self._client_id = result["client_id"]
        return result

    def proxy_start(self):
        return self._http(requests.post, f"/{self._client_id}/proxy/start")

    def proxy_status(self):
        return self._http(requests.get, f"/{self._client_id}/proxy/status")

    def proxy_stop(self):
        return self._http(requests.post, f"/{self._client_id}/proxy/stop")
