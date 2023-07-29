import pytest
from manageritm.server import create_app

@pytest.fixture(scope="function")
def app(mocker):

    def mocked_open_log_files(self):
        pass

    mocker.patch('manageritm.server.process_minder.ProcessMinder._open_log_files', mocked_open_log_files)

    app = create_app('flask_config_testing.py')

    with app.test_client() as test_client:
        with app.app_context():
            yield test_client


@pytest.fixture(scope="function")
def app_with_client(app):

    response = app.post('/client/proxy', json={})
    result = response.json
    client_id = result["client_id"]

    yield (app, client_id)

    response = app.post(f'/{client_id}/stop')


@pytest.fixture(scope="function")
def app_with_process(app_with_client):

    (app, client_id) = app_with_client

    response = app.post(f'/{client_id}/start')

    return (app, client_id)
