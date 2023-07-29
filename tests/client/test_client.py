import pytest
import uuid

from manageritm.client import ManagerITMProxyClient

class TestClient:

    @pytest.fixture(scope="function", autouse=True)
    def setup(self):
        self.base_uri = "https://localhost:5000"


    @pytest.fixture(scope="function")
    def client(self, requests_mock):
        self.client_id = str(uuid.uuid4())
        requests_mock.post(f"{self.base_uri}/client/proxy", status_code=200, json={'client_id': self.client_id})
        # not sure why this mock doesn't prevent the
        # client's __del__() function from failing
        #requests_mock.get(f"{self.base_uri}/{self.client_id}/status", status_code=200, json={'status': None})
        client = ManagerITMProxyClient(self.base_uri)
        client.client()

        yield client

        client._client_id = None
        del client
        client = None


    def test_get_client_default_ports(self, requests_mock):
        expected_status = 200
        expected_data = {'client_id': str(uuid.uuid4())}
        requests_mock.post(f"{self.base_uri}/client/proxy", status_code=expected_status, json=expected_data)
        requests_mock.get(f"{self.base_uri}/{expected_data['client_id']}/status", status_code=200, json={'status': None})

        client = ManagerITMProxyClient(self.base_uri)
        actual_data = client.client()

        assert actual_data == expected_data
        assert client._uri == self.base_uri
        assert client._client_id == expected_data['client_id']

    def test_get_client_set_port(self, requests_mock):
        expected_status = 200
        expected_data = {
            'client_id': str(uuid.uuid4()),
            'port': 5200,
            'webport': 5201,
        }
        requests_mock.post(f"{self.base_uri}/client/proxy", status_code=expected_status, json=expected_data)
        requests_mock.get(f"{self.base_uri}/{expected_data['client_id']}/status", status_code=200, json={'status': None})

        client = ManagerITMProxyClient(self.base_uri)
        actual_data = client.client(port=5200)

        assert actual_data == expected_data
        assert client._uri == self.base_uri
        assert client._client_id == expected_data['client_id']

    def test_get_client_set_webport(self, requests_mock):
        expected_status = 200
        expected_data = {
            'client_id': str(uuid.uuid4()),
            'port': 5200,
            'webport': 5201,
        }
        requests_mock.post(f"{self.base_uri}/client/proxy", status_code=expected_status, json=expected_data)
        requests_mock.get(f"{self.base_uri}/{expected_data['client_id']}/status", status_code=200, json={'status': None})

        client = ManagerITMProxyClient(self.base_uri)
        actual_data = client.client(webport=5201)

        assert actual_data == expected_data
        assert client._uri == self.base_uri
        assert client._client_id == expected_data['client_id']

    def test_get_client_set_all_ports(self, requests_mock):
        expected_status = 200
        expected_data = {
            'client_id': str(uuid.uuid4()),
            'port': 5200,
            'webport': 5201,
        }
        requests_mock.post(f"{self.base_uri}/client/proxy", status_code=expected_status, json=expected_data)
        requests_mock.get(f"{self.base_uri}/{expected_data['client_id']}/status", status_code=200, json={'status': None})

        client = ManagerITMProxyClient(self.base_uri)
        actual_data = client.client(port=5200, webport=5201)

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
    def test_start(self, requests_mock, exit_status, client):

        expected_status = 200
        expected_data = {"status": exit_status}
        requests_mock.post(f"{self.base_uri}/{self.client_id}/start", status_code=expected_status, json=expected_data)

        actual_data = client.start()

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
    def test_status(self, requests_mock, exit_status, client):

        expected_status = 200
        expected_data = {"status": exit_status}
        requests_mock.get(f"{self.base_uri}/{self.client_id}/status", status_code=expected_status, json=expected_data)

        actual_data = client.status()

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
    def test_stop(self, requests_mock, exit_status, client):

        expected_status = 200
        expected_data = {"status": exit_status}
        requests_mock.post(f"{self.base_uri}/{self.client_id}/stop", status_code=expected_status, json=expected_data)

        actual_data = client.stop()

        assert actual_data == expected_data
