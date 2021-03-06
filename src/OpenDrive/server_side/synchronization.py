"""
:module: OpenDrive.server_side.synchronization
:synopsis: Server side synchronization
:author: Julian Sobott


public functions
----------------

.. autofunction:: get_changes

private functions
-----------------


"""
from typing import List, Dict

import pynetworking as net
import os

from OpenDrive import net_interface
from OpenDrive.general import file_changes_json as gen_json
from OpenDrive.server_side import paths as server_paths
from OpenDrive.server_side import path_utils
from OpenDrive.server_side import file_exchanges
from OpenDrive.server_side import file_changes_json as server_json
from OpenDrive.server_side import database as db
from OpenDrive.general.file_exchanges import SyncAction
from OpenDrive.server_side.decorators import requires_authentication
from OpenDrive.server_side.od_logging import client_logger_sync


@requires_authentication
def get_changes(dest_path: str) -> net.File:
    user = net_interface.get_user()
    user_path = path_utils.get_users_root_folder(user.user_id)
    changes_path = server_paths.normalize_path(user_path, f"changes_{user.device_id}.json")
    return net.File(changes_path, dest_path)


@requires_authentication
def execute_actions(actions: List[SyncAction]) -> None:
    client_logger_sync().info(f"Executing actions: {actions}")
    user = net_interface.get_user()
    devices = db.Device.get_by_user_id(user.user_id)
    device_ids = [device.device_id for device in devices]
    device_ids.remove(user.device_id)

    for action in actions:
        if action["rel_file_path"] in ["", "."]:
            dest_path = action["local_folder_path"]
        else:
            dest_path = server_paths.normalize_path(action["local_folder_path"], action["rel_file_path"])
        if action["action_type"] == gen_json.ACTION_DELETE[0]:
            # Because directory deletions are also handled as files, there is only one function, that tries what
            # function fits
            file_exchanges.remove_file_dir(dest_path)
        elif action["action_type"] == gen_json.ACTION_MOVE[0]:
            src_path = server_paths.normalize_path(action["local_folder_path"], action["rel_old_file_path"])
            file_exchanges.move(src_path, dest_path)
        elif action["action_type"] == gen_json.ACTION_PULL[0]:
            src_path = action["remote_abs_path"]
            if action["is_directory"]:
                file_exchanges.pull_dir(src_path, dest_path)
            else:
                file_exchanges.pull_file(src_path, dest_path)
        elif action["action_type"] == gen_json.ACTION_MKDIR[0]:
            file_exchanges.make_dirs(dest_path)
        else:
            raise KeyError(f"Unknown action type: {action['action_type']} in {action}")

        server_json.distribute_action(action, device_ids)

    if len(actions) > 0:
        notify_other_devices(user)


def notify_other_devices(user: 'net_interface.ClientCommunicator'):
    clients: Dict[int, net_interface.ClientCommunicator] = net.ClientManager().clients
    for client in clients.values():
        if client.user_id == user.user_id and client.device_id != user.device_id:
            client_logger_sync().info(f"Trigger server synchronization: client={client}")
            client.remote_functions.trigger_server_synchronization()
