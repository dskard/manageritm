import logging
import uuid

from subprocess import Popen, PIPE, TimeoutExpired


logger = logging.getLogger(__name__)


class ProcessMinder:

    def __init__(self, command=None):

        self.client_id = str(uuid.uuid4())
        self.command = command
        self.process = None

        logger.debug(f"created new client {self.client_id}")



    def start(self):

        self.process = Popen(self.command, stdout=PIPE, stderr=PIPE)
        logger.debug(f"{self.client_id} started process with pid: {self.process.pid}")
        logger.debug(f"{self.client_id} command: {self.command}")


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


    def status(self):

        #import time; time.sleep(5)
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


