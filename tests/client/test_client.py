import pytest
import uuid

from manageritm.client import ManagerITMClient

class TestClient:

    @pytest.fixture(scope="function", autouse=True)
    def setup(self):
        self.base_uri = "https://localhost:5000"


    @pytest.fixture(scope="function")
    def client(self, requests_mock):
        self.client_id = str(uuid.uuid4())
        requests_mock.get(f"{self.base_uri}/client", status_code=200, json={'client_id': self.client_id})
        # not sure why this mock doesn't prevent the
        # client's __del__() function from failing
        #requests_mock.get(f"{self.base_uri}/{self.client_id}/proxy/status", status_code=200, json={'status': None})
        client = ManagerITMClient(self.base_uri)
        client.client()

        yield client

        client._client_id = None
        del client
        client = None


    def test_get_client(self, requests_mock):
        expected_status = 200
        expected_data = {'client_id': str(uuid.uuid4())}
        requests_mock.get(f"{self.base_uri}/client", status_code=expected_status, json=expected_data)
        requests_mock.get(f"{self.base_uri}/{expected_data['client_id']}/proxy/status", status_code=200, json={'status': None})

        client = ManagerITMClient(self.base_uri)
        actual_data = client.client()

        assert actual_data == expected_data
        assert client._uri == self.base_uri
        assert client._client_id == expected_data['client_id']


    @pytest.mark.parametrize(
        "exit_status",
        [
            0,
            -1,
            1,
            None,
        ],
        ids = [
            "exited_successfully",
            "exited_with_error",
            "error_starting",
            "running",
        ]
    )
    def test_proxy_start(self, requests_mock, exit_status, client):

        expected_status = 200
        expected_data = {"status": exit_status}
        requests_mock.post(f"{self.base_uri}/{self.client_id}/proxy/start", status_code=expected_status, json=expected_data)

        actual_data = client.proxy_start()

        assert actual_data == expected_data


    @pytest.mark.parametrize(
        "exit_status",
        [
            0,
            -1,
            1,
            None,
        ],
        ids = [
            "exited_successfully",
            "exited_with_error",
            "error_starting",
            "running",
        ]
    )
    def test_proxy_status(self, requests_mock, exit_status, client):

        expected_status = 200
        expected_data = {"status": exit_status}
        requests_mock.get(f"{self.base_uri}/{self.client_id}/proxy/status", status_code=expected_status, json=expected_data)

        actual_data = client.proxy_status()

        assert actual_data == expected_data


    @pytest.mark.parametrize(
        "exit_status",
        [
            0,
            -1,
            1,
            None,
        ],
        ids = [
            "exited_successfully",
            "exited_with_error",
            "error_starting",
            "running",
        ]
    )
    def test_proxy_stop(self, requests_mock, exit_status, client):

        expected_status = 200
        expected_data = {"status": exit_status}
        requests_mock.post(f"{self.base_uri}/{self.client_id}/proxy/stop", status_code=expected_status, json=expected_data)

        actual_data = client.proxy_stop()

        assert actual_data == expected_data
