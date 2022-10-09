import logging
import os
import random
import socket

from flask import Blueprint, current_app, request
from .process_minder import ProcessMinder


bp = Blueprint('routes', __name__)
proxies = dict()


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


@bp.route("/client", methods=["GET"])
def client():
    current_app.logger.info(f"creating a new client")
    current_app.logger.debug(f"query args: {request.args.to_dict()}")

    args = request.args
    user_provided_port = args.get("port", type=int)
    user_provided_webport = args.get("webport", type=int)

    result = dict(
        client_id=None,
        port=None,
        webport=None,
        har=None
    )

    # find an open port
    # port may not be open when we start the server
    port_lower_bound = 5200
    port_upper_bound = 5299

    if user_provided_port is None:
        port = find_open_port(port_lower_bound, port_upper_bound)
        if port is None:
            current_app.logger.info(f"could not find an open port in the range {port_lower_bound}-{port_upper_bound}")
            return result
    else:
        port = user_provided_port

    if user_provided_webport is None:
        webport = find_open_port(port_lower_bound, port_upper_bound)
        if webport is None:
            current_app.logger.info(f"could not find an open webport in the range {port_lower_bound}-{port_upper_bound}")
            return result
    else:
        webport = user_provided_webport

    mitmproxy_scripts_dir = os.path.abspath(os.path.join(current_app.root_path, "scripts"))
    har_dump_script_path = os.path.join(mitmproxy_scripts_dir, "har_dump.py")
    har_dump_directory = "./hars"

    # create hars directory if it doesnt exist
    if not os.path.exists(har_dump_directory):
        os.makedirs(har_dump_directory)

    m = ProcessMinder()

    har_filename = f"dump-{m.client_id}.har"
    har_file_path = os.path.join(har_dump_directory, har_filename)

    m.command = [
        "mitmweb",
        "-s", har_dump_script_path,
        "--set", f"hardump={har_file_path}",
        "--listen-port", f"{port}",
        "--web-host", "0.0.0.0",
        "--web-port", f"{webport}",
        "--no-web-open-browser"
    ]

    proxies[m.client_id] = m
    result["client_id"] = m.client_id
    result["port"] = port
    result["webport"] = webport
    result["har"] = har_file_path

    return result


@bp.route("/<client_id>/proxy/start", methods=["POST"])
def proxy_start(client_id):
    current_app.logger.info(f"{client_id} starting a proxy process")

    # if status is:
    # 0 -> process exited successfully
    # positive -> process exited with error
    # negative -> error starting process
    # None -> process is still running
    result = dict(
        status=-1
    )

    # check if the client_id exists
    if client_id not in proxies:
        current_app.logger.info(f"{client_id} client id does not exist")
        return result

    # start the proxy
    proxies[client_id].start()
    result["status"] = proxies[client_id].status()

    return result


@bp.route("/<client_id>/proxy/status", methods=["GET"])
def proxy_status(client_id):
    current_app.logger.info(f"{client_id} retrieving proxy status")

    # if status is:
    # 0 -> process exited successfully
    # positive -> process exited with error
    # -1 -> error retrieving process status
    # negative -> process was sent a signal
    # None -> process is still running
    result = dict(
        status=-1
    )

    # check if the client_id exists
    if client_id not in proxies:
        current_app.logger.info(f"{client_id} client id does not exist")
        return result

    # check the process status
    returncode = proxies[client_id].status()
    result["status"] = returncode

    return result


@bp.route("/<client_id>/proxy/stop", methods=["POST"])
def proxy_stop(client_id):
    current_app.logger.info(f"{client_id} stopping proxy process")

    # if status is:
    # 0 -> process exited successfully
    # positive -> process exited with error
    # negative -> error retrieving process status
    # None -> process is still running
    result = dict(
        status=-1
    )

    # check if the id exists
    if client_id not in proxies:
        current_app.logger.info(f"{client_id} client id does not exist")
        return result

    # terminate the proxy process
    proxies[client_id].stop()
    result["status"] = proxies[client_id].status()

    return result
