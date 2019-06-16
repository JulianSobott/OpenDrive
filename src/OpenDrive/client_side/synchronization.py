"""
:module: OpenDrive.client_side.synchronization
:synopsis: Synchronisation process between the server and client
:author: Julian Sobott


public functions
-----------------

.. autofunction:: full_synchronize
.. autofunction:: create_action
.. autofunction:: execute_client_actions


private functions
------------------

.. autofunction:: _get_server_changes
.. autofunction:: _get_client_changes
.. autofunction:: _merge_changes
.. autofunction:: _execute_server_actions

"""
import json
import os
from typing import List

from OpenDrive import net_interface
from OpenDrive.client_side import file_changes as c_file_changes
from OpenDrive.client_side import file_changes_json as client_json
from OpenDrive.client_side import paths as client_paths
from OpenDrive.client_side.od_logging import logger
from OpenDrive.general import file_changes_json as gen_json
from OpenDrive.general import file_exchanges as gen_file_exchanges
from OpenDrive.general.file_exchanges import SyncAction
from OpenDrive.general.paths import NormalizedPath


def full_synchronize() -> None:
    """Starts a sync process, where changes from server and client are merged."""
    server_changes = _get_server_changes()
    client_changes = _get_client_changes()
    start_synchronization = gen_json.get_current_timestamp()
    server_actions, client_actions, conflicts = _merge_changes(server_changes, client_changes)
    _execute_server_actions(server_actions)
    execute_client_actions(client_actions)
    gen_json.remove_handled_changes(start_synchronization)
    net_interface.server.remove_handled_changes(start_synchronization)
    if len(conflicts) > 0:
        logger.error(f"Unhandled conflicts: {conflicts}")


def trigger_server_synchronization():
    """Called from the server, when there were changes at the server."""
    c_file_changes.sync_waiter.sync()


def _get_server_changes() -> dict:
    dest_path = os.path.join(client_paths.LOCAL_CLIENT_DATA, "server_changes.json")
    changes_file = net_interface.server.get_changes(dest_path)
    with open(changes_file.dst_path, "r") as file:
        return json.load(file)


def _get_client_changes() -> dict:
    return client_json.get_all_data()


def _merge_changes(server_changes: dict, client_changes: dict) -> tuple:
    """Merges the changes from both sides based on their paths/names. If both sides have a change in the same file,
    these changes are added as conflict.
    """
    needed_client_actions = []
    needed_server_actions = []
    conflicts = []

    while len(client_changes.keys()) > 0:
        c_folder_path, client_folder = client_changes.popitem()
        s_folder_path = client_folder["server_folder_path"]
        server_folder = server_changes[s_folder_path]
        server_actions, new_conflicts = _calculate_remote_actions(client_folder, server_folder, c_folder_path,
                                                                  s_folder_path)
        needed_server_actions += server_actions
        conflicts += new_conflicts
        client_actions, new_conflicts = _calculate_remote_actions(server_folder, client_folder, s_folder_path,
                                                                  c_folder_path)
        needed_client_actions += client_actions
        conflicts += new_conflicts

    return needed_server_actions, needed_client_actions, conflicts


def _calculate_remote_actions(local_folder: dict, remote_folder: dict, local_folder_path: client_paths.NormalizedPath,
                              remote_folder_path: client_paths.NormalizedPath):
    needed_remote_actions = []
    conflicts = []

    for l_file_path, l_file in local_folder["changes"].items():
        if l_file_path in remote_folder["changes"].keys():
            conflicts.append({"folders": [local_folder_path, remote_folder_path],
                              "rel_file_path": l_file_path,
                              "local_file": l_file,
                              "remote_file": remote_folder["changes"][l_file_path]})
            remote_folder["changes"].pop(l_file_path)
        else:
            if l_file["action"] == gen_json.ACTION_PULL[0]:
                remote_abs_path = client_paths.normalize_path(local_folder_path, l_file_path)
            else:
                remote_abs_path = None
            action = create_action(remote_folder_path, l_file_path, gen_json.ActionType((l_file["action"], 0)),
                                   l_file["is_directory"],
                                   l_file["rel_old_file_path"], remote_abs_path)
            needed_remote_actions.append(action)

    return needed_remote_actions, conflicts


def execute_client_actions(client_actions: List[SyncAction]) -> None:
    for action in client_actions:
        dest_path = os.path.join(action["local_folder_path"], action["rel_file_path"])
        if action["action_type"] == gen_json.ACTION_DELETE[0]:
            # Because directory deletions are also handled as files, there is only one function, that tries what
            # function fits
            if os.path.isdir(dest_path):
                gen_file_exchanges.remove_dir(dest_path)
            else:
                gen_file_exchanges.remove_file(dest_path)
        elif action["action_type"] == gen_json.ACTION_MOVE[0]:
            src_path = os.path.join(action["local_folder_path"], action["rel_old_file_path"])
            gen_file_exchanges.move(src_path, dest_path)
        elif action["action_type"] == gen_json.ACTION_PULL[0]:
            src_path = action["remote_abs_path"]
            if action["is_directory"]:
                net_interface.server.get_dir(src_path, dest_path)
            else:
                net_interface.server.get_file(src_path, dest_path)
        elif action["action_type"] == gen_json.ACTION_MKDIR[0]:
            gen_file_exchanges.make_dirs(dest_path)
        else:
            raise KeyError(f"Unknown action type: {action['action_type']} in {action}")


def _execute_server_actions(server_actions: List[SyncAction]) -> None:
    net_interface.server.execute_actions(server_actions)


def create_action(local_folder_path: NormalizedPath, rel_file_path: NormalizedPath, action_type: gen_json.ActionType,
                  is_directory: bool = False, rel_old_file_path: NormalizedPath = None,
                  remote_abs_path: str = None) -> SyncAction:
    sync_action = {"local_folder_path": local_folder_path,  # folder key. To create abs_path of file
                   "rel_file_path": rel_file_path,  # changes key at pull, delete. destination
                   "action_type": action_type[0],  # pull, move, delete
                   "is_directory": is_directory,  # bool
                   "rel_old_file_path": rel_old_file_path,  # optional. changes key at move. source at move
                   "remote_abs_path": remote_abs_path  # source at pull.
                   }
    return SyncAction(sync_action)
