import random
import socket


def find_open_port(lower_bound=None, upper_bound=None, max_attempts=100):
    """search for an open port within a range

    make max_attempts tries to find an open port between
    lower_bound and upper_bound.

    return the port number on success
    return None on failure
    """

    attempts = 0
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = None

    while attempts < max_attempts and port is None:
        attempts += 1
        if lower_bound is not None and upper_bound is not None:
            port = random.randint(lower_bound, upper_bound)
        else:
            port = 0

        try:
            sock.bind(('', port))
        except:
            # socket error is raised if bind fails
            port = None

        if port == 0:
            _, port = sock.getsockname()

    sock.close()

    return port
