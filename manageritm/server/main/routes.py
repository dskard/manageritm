from flask import current_app
from manageritm.server.main import bp
from manageritm.server.processes import processes


@bp.route("/<client_id>/start", methods=["POST"])
def start(client_id):
    current_app.logger.info(f"{client_id} starting a process")

    # if status is:
    # 0 -> process exited successfully
    # positive -> process exited with error
    # negative -> error starting process
    # None -> process is still running
    result = dict(
        status=-1
    )

    # check if the client_id exists
    if client_id not in processes:
        current_app.logger.info(f"{client_id} client id does not exist")
        return result

    # start the process
    processes[client_id].start()
    result["status"] = processes[client_id].status()

    return result


@bp.route("/<client_id>/status", methods=["GET"])
def status(client_id):
    current_app.logger.info(f"{client_id} retrieving status")

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
    if client_id not in processes:
        current_app.logger.info(f"{client_id} client id does not exist")
        return result

    # check the process status
    returncode = processes[client_id].status()
    result["status"] = returncode

    return result


@bp.route("/<client_id>/stop", methods=["POST"])
def stop(client_id):
    current_app.logger.info(f"{client_id} stopping process")

    # if status is:
    # 0 -> process exited successfully
    # positive -> process exited with error
    # negative -> error retrieving process status
    # None -> process is still running
    result = dict(
        status=-1
    )

    # check if the id exists
    if client_id not in processes:
        current_app.logger.info(f"{client_id} client id does not exist")
        return result

    # terminate the process
    processes[client_id].stop()
    result["status"] = processes[client_id].status()

    return result
