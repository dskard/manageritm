import os

from flask import current_app, request, Response
from jsonschema import validate, ValidationError
from manageritm.server.client import bp
from manageritm.server.process_minder import ProcessMinder
from manageritm.server.processes import processes
from manageritm.server.utils import find_open_port

@bp.route("/proxy", methods=["POST"])
def proxy_client():
    current_app.logger.info(f"creating a new proxy client")

    user_provided_data = request.get_json()

    current_app.logger.debug(f"json data: {user_provided_data}")

    schema = {
        "type" : "object",
        "properties" : {
            "port" : {"type" : "integer"},
            "webport" : {"type" : "integer"},
            "har" : {"type" : "string"},
        },
    }

    try:
        validate(instance=user_provided_data, schema=schema)
    except ValidationError as e:
        return Response(e.message, status=400)

    user_provided_port = None
    if 'port' in user_provided_data:
        user_provided_port = user_provided_data['port']

    user_provided_webport = None
    if 'webport' in user_provided_data:
        user_provided_webport = user_provided_data['webport']

    user_provided_har = None
    if 'har' in user_provided_data:
        user_provided_har = user_provided_data['har']

    result = dict(
        client_id=None,
        port=None,
        webport=None,
        har=None
    )

    # find an open port
    # port may not be open when we start the server
    port_lower_bound = current_app.config['MANAGERITM_PROXY_PORT_LOWER_BOUND']
    port_upper_bound = current_app.config['MANAGERITM_PROXY_PORT_UPPER_BOUND']

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
    har_dump_directory = current_app.config['MANAGERITM_PROXY_HARS_DIR']

    # create hars directory if it doesnt exist
    if not os.path.exists(har_dump_directory):
        os.makedirs(har_dump_directory)

    m = ProcessMinder()

    if user_provided_har is None:
        har_filename = f"dump-{m.client_id}.har"
    else:
        har_filename = user_provided_har

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

    processes[m.client_id] = m
    result["client_id"] = m.client_id
    result["port"] = port
    result["webport"] = webport
    result["har"] = har_file_path

    return result

@bp.route("/command", methods=["POST"])
def command_client():
    current_app.logger.info(f"creating a new command client")

    user_provided_data = request.get_json()

    current_app.logger.debug(f"json data: {user_provided_data}")

    schema = {
        "type" : "object",
        "properties" : {
            "env" : {"type" : "object"},
            "additional_env" : {"type" : "object"},
        },
    }

    try:
        validate(instance=user_provided_data, schema=schema)
    except ValidationError as e:
        return Response(e.message, status=400)


    command = current_app.config['MANAGERITM_CLIENT_COMMAND']

    env = None
    if 'env' in user_provided_data:
        env = user_provided_data['env']

    additional_env = None
    if 'additional_env' in user_provided_data:
        additional_env = user_provided_data['additional_env']


    result = dict(
        client_id=None,
    )

    m = ProcessMinder(
        command = command,
        env = env,
        additional_env = additional_env,
    )

    processes[m.client_id] = m
    result["client_id"] = m.client_id

    return result
