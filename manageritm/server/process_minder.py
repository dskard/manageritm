import logging
import os
import uuid

from flask import current_app
from subprocess import Popen, PIPE, STDOUT, TimeoutExpired
from pathlib import Path


logger = logging.getLogger(__name__)


class ProcessMinder:

    def __init__(self, command=None, env=None, additional_env=None):

        self.client_id = str(uuid.uuid4())
        self.command = command
        self.process = None
        self.log = None

        self.env = env
        self.additional_env = additional_env

        logger.debug(f"created new client {self.client_id}")


    def __del__(self):

        if self.status() is None:
            self.stop()

        # close logs incase the process was started
        # but exited without closing the logs.
        self._close_log_files()


    def _open_log_files(self):

        if self.log is not None:
            self._close_log_files()

        # setup the name of the log file
        log_path = Path(current_app.config['MANAGERITM_LOG_DIR'],f"{self.client_id}.log")

        # make sure the parent directory exists
        log_path.parent.mkdir(exist_ok=True)

        self.log = open(log_path, "wb", 0)


    def _close_log_files(self):

        if self.log is not None:
            self.log.close()
            self.log = None


    def start(self):

        self._open_log_files()

        if self.additional_env is not None:
            # user provided additional environment vars
            # check if they provided default environment vars
            if self.env is None:
                # no default environment vars provided
                # get the process' environment vars
                # because if we provide Popen any environment vars,
                # we have to provide all environment vars
                self.env = os.environ
            # merge the user's additional environment vars in
            self.env |= self.additional_env

        self.process = Popen(self.command, stdout=self.log, stderr=STDOUT, env=self.env)
        logger.debug(f"{self.client_id} started process with pid: {self.process.pid}")
        logger.debug(f"{self.client_id} command: {self.command}")
        logger.debug(f"{self.client_id} writing logs to {self.log}")


    def stop(self):

        # try terminating the process
        self.process.terminate()
        try:
            self.process.wait(10)
        except TimeoutExpired as e:
            # try killing the process
            self.process.kill()
            self.process.wait()

        logger.debug(f"{self.client_id} stopped process pid {self.process.pid}")
        logger.debug(f"{self.client_id} process exit status: {self.process.returncode}")

        self._close_log_files()


    def status(self):

        if self.process is None:
            logger.info(f"{self.client_id} process has not been started")
            return -1

        returncode = self.process.poll()

        logger.info(f"{self.client_id} process returncode: {returncode}")

        if returncode is None:
            logger.info(f"{self.client_id} process {self.process.pid} is still running")
        else:
            logger.info(f"{self.client_id} process {self.process.pid} has ended")

        return returncode


