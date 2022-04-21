from manageritm.server.routes import find_open_port

class TestRoutes:

    def test_get_client(self, app):

        response = app.get('/client')

        assert response.status_code == 200

        result = response.json
        assert result["client_id"] is not None
        assert result["port"] is not None
        assert result["har"] is not None


    def test_start_process(self, app_with_client):

        (app, client_id) = app_with_client

        response = app.post(f'/{client_id}/proxy/start')
        assert response.status_code == 200

        result = response.json
        assert result["status"] is None


    def test_process_status(self, app_with_process):

        (app, client_id) = app_with_process

        response = app.get(f'/{client_id}/proxy/status')
        assert response.status_code == 200

        result = response.json
        assert result["status"] is None


    def test_stop_process(self, app_with_process):

        (app, client_id) = app_with_process

        response = app.post(f'/{client_id}/proxy/stop')
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
            def __init__(self,*args,**kwargs):
                self.args = args
                self.kwargs = kwargs

            def bind(self, arg):
                pass

            def close(self):
                pass

            def getsockname(self):
                return None, expected_port

        mocker.patch('manageritm.server.routes.socket.socket', MockedSocket)


        actual_port = find_open_port()

        assert actual_port == expected_port


    def test_find_port_lower_bound_only(self, mocker):
        """with only a lower bound, no range is considered"""

        expected_port = 4321

        class MockedSocket:
            def __init__(self,*args,**kwargs):
                self.args = args
                self.kwargs = kwargs
                self.port = expected_port

            def bind(self, arg):
                # bind will be called with a port.
                # we expect the port to be 0 because only lower bound was given
                # if it is non-zero, overwrite our expected_port in self.port
                # so that the provided port is returned by getsockname()
                (host,port) = arg
                if port != 0:
                    self.port = port

            def close(self):
                pass

            def getsockname(self):
                return None, self.port

        mocker.patch('manageritm.server.routes.socket.socket', MockedSocket)


        actual_port = find_open_port(lower_bound=5000)

        assert actual_port == expected_port


    def test_find_port_upper_bound_only(self, mocker):
        """with only an upper bound, no range is considered"""

        expected_port = 4321

        class MockedSocket:
            def __init__(self,*args,**kwargs):
                self.args = args
                self.kwargs = kwargs
                self.port = expected_port

            def bind(self, arg):
                # bind will be called with a port.
                # we expect the port to be 0 because only lower bound was given
                # if it is non-zero, overwrite our expected_port in self.port
                # so that the provided port is returned by getsockname()
                (host,port) = arg
                if port != 0:
                    self.port = port

            def close(self):
                pass

            def getsockname(self):
                return None, self.port

        mocker.patch('manageritm.server.routes.socket.socket', MockedSocket)


        actual_port = find_open_port(upper_bound=4000)

        assert actual_port == expected_port


    def test_find_port_lower_and_upper_bound(self, mocker):
        """with lower and upper bounds, a random port is chosen"""

        unexpected_port = 4321

        class MockedSocket:
            def __init__(self,*args,**kwargs):
                self.args = args
                self.kwargs = kwargs
                self.port = unexpected_port

            def bind(self, arg):
                # bind will be called with a port.
                # we expect the port to be non-zero because both lower and
                # upper bounds were given.
                # if it is non-zero, overwrite our unexpected_port in self.port
                # so that the provided port is returned by getsockname()
                (host,port) = arg
                if port != 0:
                    self.port = port

            def close(self):
                pass

            def getsockname(self):
                return None, self.port

        mocker.patch('manageritm.server.routes.socket.socket', MockedSocket)


        lower_bound = 5000
        upper_bound = 5099
        actual_port = find_open_port(lower_bound=lower_bound, upper_bound=upper_bound)

        assert actual_port != unexpected_port
        assert actual_port >= lower_bound
        assert actual_port <= upper_bound


    def test_find_port_max_attempts(self, mocker):

        class MockedSocket:
            bind_call_count = 0
            def __init__(self,*args,**kwargs):
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

        mocker.patch('manageritm.server.routes.socket.socket', MockedSocket)


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
            def __init__(self,*args,**kwargs):
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
                (host,port) = arg
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

        mocker.patch('manageritm.server.routes.socket.socket', MockedSocket)


        lower_bound = 5000
        upper_bound = 5099
        max_attempts = 5
        actual_port = find_open_port(lower_bound=lower_bound, upper_bound=upper_bound, max_attempts=max_attempts)

        assert actual_port != unexpected_port
        assert actual_port >= lower_bound
        assert actual_port <= upper_bound
        # we should call bind 3 times, 2 failed binds and 1 successful bind
        assert MockedSocket.bind_call_count == 3
