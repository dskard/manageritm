from manageritm.server.process_minder import ProcessMinder
from subprocess import Popen, PIPE, TimeoutExpired

class TestProcessMinder:

    def test_start(self, mocker):

        class MockedPopen:
            def __init__(self,command,**args):
                self.command = command
                self.args = args
                self.pid = 400

        class MockedPipe:
            pass

        mocker.patch('manageritm.server.process_minder.Popen', MockedPopen)
        mocker.patch('manageritm.server.process_minder.PIPE', MockedPipe)

        command = "my_command"
        pm = ProcessMinder(command)

        # call the start() function
        pm.start()

        # check that Popen was called with the correct args to start a process
        assert pm.process.command == command
        assert pm.process.args["stdout"] == MockedPipe
        assert pm.process.args["stderr"] == MockedPipe


    def test_stop_terminate(self, mocker):

        class MockedPopen:
            def __init__(self,command,**args):
                self.command = command
                self.args = args
                self.pid = 400
                self.returncode = None
            def terminate(self):
                pass
            def wait(self,s=5):
                self.returncode = 0
            def kill(self):
                self.returncode = 1

        mocker.patch('manageritm.server.process_minder.Popen', MockedPopen)

        command = "my_command"
        pm = ProcessMinder(command)
        pm.start()

        # setup spies so we can count function calls
        terminate_spy = mocker.spy(pm.process, 'terminate')
        wait_spy = mocker.spy(pm.process, 'wait')
        kill_spy = mocker.spy(pm.process, 'kill')

        # call the stop() function
        pm.stop()

        # check that the terminate() and wait() functions were called,
        # check that kill() was not called
        assert pm.process.returncode == 0
        assert terminate_spy.call_count == 1
        assert wait_spy.call_count == 1
        assert kill_spy.call_count == 0


    def test_stop_kill(self, mocker):

        class MockedPopen:
            def __init__(self,command,**args):
                self.command = command
                self.args = args
                self.pid = 400
                self.returncode = None
                self._raise_exception = True
            def terminate(self):
                pass
            def wait(self,s=5):
                if self._raise_exception is True:
                    self._raise_exception = False
                    self.returncode = 0
                    raise TimeoutExpired(cmd=self.command,timeout=s)
                else:
                    self._raise_exception = True
            def kill(self):
                self.returncode = 1

        mocker.patch('manageritm.server.process_minder.Popen', MockedPopen)

        command = "my_command"
        pm = ProcessMinder(command)
        pm.start()

        # setup spies so we can count function calls
        terminate_spy = mocker.spy(pm.process, 'terminate')
        wait_spy = mocker.spy(pm.process, 'wait')
        kill_spy = mocker.spy(pm.process, 'kill')

        # call the stop() function
        pm.stop()

        # check that the terminate(), wait() and kill() functions were called
        assert pm.process.returncode == 1
        assert terminate_spy.call_count == 1
        assert wait_spy.call_count == 2
        assert kill_spy.call_count == 1


    def test_status_process_not_started(self, mocker):

        command = "my_command"
        pm = ProcessMinder(command)

        # don't start the process
        # call the status() function
        status = pm.status()

        # check that the value returned by status is -1
        assert status == -1


    def test_status_process_running(self, mocker):

        class MockedPopen:
            def __init__(self,command,**args):
                self.command = command
                self.args = args
                self.pid = 400
                self.returncode = -2
            def poll(self):
                self.returncode = None
                return self.returncode

        mocker.patch('manageritm.server.process_minder.Popen', MockedPopen)

        command = "my_command"
        pm = ProcessMinder(command)
        pm.start()

        # setup spies so we can count function calls
        poll_spy = mocker.spy(pm.process, 'poll')

        # call the stop() function
        pm.status()

        # check that the terminate(), wait() and kill() functions were called
        assert pm.process.returncode is None
        assert poll_spy.call_count == 1


    def test_status_process_exited(self, mocker):

        class MockedPopen:
            def __init__(self,command,**args):
                self.command = command
                self.args = args
                self.pid = 400
                self.returncode = -2
            def poll(self):
                self.returncode = 0
                return self.returncode

        mocker.patch('manageritm.server.process_minder.Popen', MockedPopen)

        command = "my_command"
        pm = ProcessMinder(command)
        pm.start()

        # setup spies so we can count function calls
        poll_spy = mocker.spy(pm.process, 'poll')

        # call the stop() function
        status = pm.status()

        # check that the poll() function is called
        assert status == 0
        assert poll_spy.call_count == 1
