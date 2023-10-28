import pytest

from manageritm.server.utils import find_open_port


class TestRoutes:

    def test_create_proxy_client_bad_port_type(self, app):
        """sending the wrong datatype for the port should return an error"""

        data = {"port": "fff"}
        response = app.post('/client/proxy', json=data)

        assert response.status_code == 400

        result = response.data
        assert result == bytes(f"'{data['port']}' is not of type 'integer'", encoding="utf-8")

    def test_create_proxy_client_find_open_ports(self, app):

        response = app.post('/client/proxy', json={})

        assert response.status_code == 200

        result = response.json
        assert result["client_id"] is not None
        assert result["port"] is not None
        assert result["webport"] is not None
        assert result["har"] is not None

    def test_create_proxy_client_user_provided_port(self, app):

        response = app.post('/client/proxy', json={'port':5200})

        assert response.status_code == 200

        result = response.json
        assert result["client_id"] is not None
        assert result["port"] == 5200
        assert result["webport"] is not None
        assert result["har"] is not None

    def test_create_proxy_client_user_provided_webport(self, app):

        response = app.post('/client/proxy', json={'webport':5200})

        assert response.status_code == 200

        result = response.json
        assert result["client_id"] is not None
        assert result["port"] is not None
        assert result["webport"] == 5200
        assert result["har"] is not None

    def test_create_proxy_client_user_provided_all_ports(self, app):

        response = app.post('/client/proxy', json={'port':5200,'webport':5201})

        assert response.status_code == 200

        result = response.json
        assert result["client_id"] is not None
        assert result["port"] == 5200
        assert result["webport"] == 5201
        assert result["har"] is not None

    def test_create_proxy_client_user_provided_additional_flags(self, app):
        """User can send additional flags to be merged with default flags"""

        data = {
            'additional_flags': ['--opt1','value1','--opt2','value2']
        }

        response = app.post('/client/proxy', json=data)

        assert response.status_code == 200

        result = response.json
        assert result["command"] is not None

        # find all of the places in the command
        # that look like they could be the additional flags we provided
        indices = [idx for idx, value in enumerate(result['command']) if value == data['additional_flags'][0]]

        # get the number of additional items we should have added to the command
        num_items = len(data['additional_flags'])

        # look through the command to find the additional flags we added
        matching_part_of_command = None
        for i in indices:
            # grab a possibly matching part of the command list
            l1 = result['command'][i:i+num_items]
            # check if this part of the command list matches our arguments
            if l1 == data['additional_flags']:
                # stop searching
                matching_part_of_command = l1
                break

        # check that we found the additional arguments we added to the command
        assert matching_part_of_command is not None

    def test_create_command_client_no_args(self, app):

        response = app.post('/client/command', json={})

        assert response.status_code == 200

        result = response.json
        assert result["client_id"] is not None

    def test_create_command_client_send_command(self, app):
        """User can send command to override default command"""

        data = {
            'command': ['sleep','200000000000']
        }

        response = app.post('/client/command', json=data)

        assert response.status_code == 200

        result = response.json
        assert result["command"] == data['command']
        assert result["client_id"] is not None

    def test_create_command_client_send_environment(self, app):
        """User can send environment to override default environment"""

        data = {
            'env': {'VARIABLE':'VALUE'}
        }

        response = app.post('/client/command', json=data)

        assert response.status_code == 200

        result = response.json
        assert result["client_id"] is not None

    def test_create_command_client_send_additional_environment(self, app):
        """User can send additional environment to be merged with default environment"""

        data = {
            'additional_env': {'VARIABLE':'VALUE'}
        }

        response = app.post('/client/command', json=data)

        assert response.status_code == 200

        result = response.json
        assert result["client_id"] is not None

    def test_create_command_client_send_environment_and_additional_environment(self, app):
        """User can send environment and additional environment to override default environment"""

        data = {
            'env': {'ORIGINAL_VARIABLE':'ORIGINAL_VALUE'},
            'additional_env': {'ADDITIONAL_VARIABLE':'ADDITIONAL_VALUE'}
        }

        response = app.post('/client/command', json=data)

        assert response.status_code == 200

        result = response.json
        assert result["client_id"] is not None

    def test_create_command_client_check_parameter_datatypes(self, app):
        """User is alerted with wrong parameter datatypes are used."""

        data = {
            'env': 123
        }

        response = app.post('/client/command', json=data)

        assert response.status_code == 400

        result = response.data
        assert result == bytes(f"{data['env']} is not of type 'object'", encoding="utf-8")

    def test_start_process(self, app_with_client):

        (app, client_id) = app_with_client

        response = app.post(f'/{client_id}/start')
        assert response.status_code == 200

        result = response.json
        assert result["status"] is None

    def test_process_status(self, app_with_process):

        (app, client_id) = app_with_process

        response = app.get(f'/{client_id}/status')
        assert response.status_code == 200

        result = response.json
        assert result["status"] is None

    def test_stop_process(self, app_with_process):

        (app, client_id) = app_with_process

        response = app.post(f'/{client_id}/stop')
        assert response.status_code == 200

        result = response.json
        # check that the process was stopped with one of:
        # * SIGKILL (-9)
        # * SIGTERM (-15)
        # not sure why it also shows up with 0 if you wait too long
        assert result["status"] in (0, -9, -15)

    def test_find_port_success_no_bounds(self, mocker):

        expected_port = 4321

        class MockedSocket:
            def __init__(self, *args, **kwargs):
                self.args = args
                self.kwargs = kwargs

            def bind(self, arg):
                pass

            def close(self):
                pass

            def getsockname(self):
                return None, expected_port

        mocker.patch('manageritm.server.utils.socket.socket', MockedSocket)

        actual_port = find_open_port()

        assert actual_port == expected_port

    def test_find_port_lower_bound_only(self, mocker):
        """with only a lower bound, no range is considered"""

        expected_port = 4321

        class MockedSocket:
            def __init__(self, *args, **kwargs):
                self.args = args
                self.kwargs = kwargs
                self.port = expected_port

            def bind(self, arg):
                # bind will be called with a port.
                # we expect the port to be 0 because only lower bound was given
                # if it is non-zero, overwrite our expected_port in self.port
                # so that the provided port is returned by getsockname()
                (host, port) = arg
                if port != 0:
                    self.port = port

            def close(self):
                pass

            def getsockname(self):
                return None, self.port

        mocker.patch('manageritm.server.utils.socket.socket', MockedSocket)

        actual_port = find_open_port(lower_bound=5000)

        assert actual_port == expected_port

    def test_find_port_upper_bound_only(self, mocker):
        """with only an upper bound, no range is considered"""

        expected_port = 4321

        class MockedSocket:
            def __init__(self, *args, **kwargs):
                self.args = args
                self.kwargs = kwargs
                self.port = expected_port

            def bind(self, arg):
                # bind will be called with a port.
                # we expect the port to be 0 because only lower bound was given
                # if it is non-zero, overwrite our expected_port in self.port
                # so that the provided port is returned by getsockname()
                (host, port) = arg
                if port != 0:
                    self.port = port

            def close(self):
                pass

            def getsockname(self):
                return None, self.port

        mocker.patch('manageritm.server.utils.socket.socket', MockedSocket)

        actual_port = find_open_port(upper_bound=4000)

        assert actual_port == expected_port

    def test_find_port_lower_and_upper_bound(self, mocker):
        """with lower and upper bounds, a random port is chosen"""

        unexpected_port = 4321

        class MockedSocket:
            def __init__(self, *args, **kwargs):
                self.args = args
                self.kwargs = kwargs
                self.port = unexpected_port

            def bind(self, arg):
                # bind will be called with a port.
                # we expect the port to be non-zero because both lower and
                # upper bounds were given.
                # if it is non-zero, overwrite our unexpected_port in self.port
                # so that the provided port is returned by getsockname()
                (host, port) = arg
                if port != 0:
                    self.port = port

            def close(self):
                pass

            def getsockname(self):
                return None, self.port

        mocker.patch('manageritm.server.utils.socket.socket', MockedSocket)

        lower_bound = 5000
        upper_bound = 5099
        actual_port = find_open_port(lower_bound=lower_bound, upper_bound=upper_bound)

        assert actual_port != unexpected_port
        assert actual_port >= lower_bound
        assert actual_port <= upper_bound

    def test_find_port_max_attempts(self, mocker):

        class MockedSocket:
            bind_call_count = 0

            def __init__(self, *args, **kwargs):
                self.args = args
                self.kwargs = kwargs

            def bind(self, arg):
                # every time the caller tries to bind,
                # raise an error to simulate the port is taken
                MockedSocket.bind_call_count += 1
                raise Error()

            def close(self):
                pass

            def getsockname(self):
                return None, self.port

        mocker.patch('manageritm.server.utils.socket.socket', MockedSocket)

        lower_bound = 5000
        upper_bound = 5099
        max_attempts = 2
        actual_port = find_open_port(lower_bound=lower_bound, upper_bound=upper_bound, max_attempts=max_attempts)

        assert actual_port is None
        assert MockedSocket.bind_call_count == max_attempts

    def test_find_port_multiple_attempts_with_range(self, mocker):

        unexpected_port = 4321

        class MockedSocket:
            bind_call_count = 0

            def __init__(self, *args, **kwargs):
                self.args = args
                self.kwargs = kwargs
                self.port = unexpected_port

            def bind(self, arg):
                # bind will be called with a port.
                # the first two times bind is called, raise error to simulate
                # failure.  the third time bind is called, set self.port to the
                # port number provided by the caller to simulate a successful
                # bind.
                # we expect the port to be non-zero because both lower and
                # upper bounds were given.
                # if it is non-zero, overwrite our unexpected_port in self.port
                # so that the provided port is returned by getsockname().
                (host, port) = arg
                MockedSocket.bind_call_count += 1
                if MockedSocket.bind_call_count < 3:
                    raise Error()
                else:
                    if port != 0:
                        self.port = port

            def close(self):
                pass

            def getsockname(self):
                return None, self.port

        mocker.patch('manageritm.server.utils.socket.socket', MockedSocket)

        lower_bound = 5000
        upper_bound = 5099
        max_attempts = 5
        actual_port = find_open_port(lower_bound=lower_bound, upper_bound=upper_bound, max_attempts=max_attempts)

        assert actual_port != unexpected_port
        assert actual_port >= lower_bound
        assert actual_port <= upper_bound
        # we should call bind 3 times, 2 failed binds and 1 successful bind
        assert MockedSocket.bind_call_count == 3
