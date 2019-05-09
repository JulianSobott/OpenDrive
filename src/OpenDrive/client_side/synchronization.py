"""
:module: OpenDrive.client_side.synchronization
:synopsis: Synchronisation process between the server and client
:author: Julian Sobott


public functions
-----------------

.. autofunction:: full_synchronize


private functions
------------------

.. autofunction:: _get_server_changes
.. autofunction:: _get_client_changes
.. autofunction:: _merge_changes
.. autofunction:: _execute_client_actions
.. autofunction:: _execute_server_actions

"""
import json
import os
from typing import Optional, NewType, List

from OpenDrive.net_interface import server
from OpenDrive.client_side import paths as client_paths
from OpenDrive.client_side import file_changes_json as client_json
from OpenDrive.general import file_changes_json as gen_json
from OpenDrive.general import file_exchanges as gen_file_exchanges
from OpenDrive.client_side.od_logging import logger

SyncAction = NewType("SyncAction", dict)


def full_synchronize() -> None:
    """Starts a sync process, where changes from server and client are merged."""
    server_changes = _get_server_changes()
    client_changes = _get_client_changes()
    server_actions, client_actions, conflicts = _merge_changes(server_changes, client_changes)
    _execute_server_actions(server_actions)
    _execute_client_actions(client_actions)
    logger.error(f"Unhandled conflicts: {conflicts}")


def _get_server_changes() -> dict:
    dest_path = os.path.join(client_paths.LOCAL_CLIENT_DATA, "server_changes.json")
    changes_file = server.get_changes(dest_path)
    with open(changes_file.dst_path, "r") as file:
        return json.load(file)


def _get_client_changes() -> dict:
    return client_json.get_all_data()


def _merge_changes(server_changes: dict, client_changes: dict) -> tuple:
    """pop items from the changes dicts, till both dicts are empty. All actions are instead distributed to the
    proper lists"""
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
            src_path = client_paths.normalize_path(os.path.join(local_folder_path, l_file_path))
            dest_path = client_paths.normalize_path(os.path.join(remote_folder_path, l_file_path))
            if gen_json.ACTION_PULL[0] == l_file["necessary_action"]:
                needed_remote_actions.append(_create_action(gen_json.ACTION_PULL, src_path, dest_path))
            elif gen_json.ACTION_MOVE[0] == l_file["necessary_action"]:
                old_path = client_paths.normalize_path(os.path.join(remote_folder_path, l_file["old_file_path"]))
                if gen_json.CHANGE_MODIFIED in l_file["changes"] or gen_json.CHANGE_CREATED[0] in l_file["changes"]:
                    needed_remote_actions.append(_create_action(gen_json.ACTION_PULL, src_path, dest_path))
                    needed_remote_actions.append(_create_action(gen_json.ACTION_DELETE, old_path))
                else:
                    needed_remote_actions.append(_create_action(gen_json.ACTION_MOVE, old_path, dest_path))
            elif gen_json.ACTION_DELETE[0] == l_file["necessary_action"]:
                needed_remote_actions.append(_create_action(gen_json.ACTION_DELETE, src_path))

    return needed_remote_actions, conflicts


def _execute_client_actions(client_actions: List[SyncAction]) -> None:
    for action in client_actions:
        if action["action_type"] == gen_json.ACTION_DELETE[0]:
            gen_file_exchanges.remove_file(action["src_path"])
        elif action["action_type"] == gen_json.ACTION_MOVE[0]:
            gen_file_exchanges.move_file(action["src_path"], action["dest_path"])
        elif action["action_type"] == gen_json.ACTION_PULL[0]:
            server.get_file(action["src_path"], action["dest_path"])
        else:
            raise KeyError(f"Unknown action type: {action['action_type']} in {action}")


def _execute_server_actions(server_actions) -> None:
    for action in server_actions:
        if action["action_type"] == gen_json.ACTION_DELETE[0]:
            server.remove_file(action["src_path"])
        elif action["action_type"] == gen_json.ACTION_MOVE[0]:
            server.move_file(action["src_path"], action["dest_path"])
        elif action["action_type"] == gen_json.ACTION_PULL[0]:
            server.pull_file(action["src_path"], action["dest_path"])
        else:
            raise KeyError(f"Unknown action type: {action['action_type']} in {action}")


def _create_action(action_type: gen_json.ActionType, src_path: gen_json.NormalizedPath,
                   dest_path: Optional[gen_json.NormalizedPath] = None) -> SyncAction:
    sync_action = {"action_type": action_type[0],
                   "src_path": src_path}
    if dest_path:
        sync_action["dest_path"] = dest_path
    return SyncAction(sync_action)
