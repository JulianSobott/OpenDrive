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
from typing import Optional

from OpenDrive.net_interface import server
from OpenDrive.client_side import paths as client_paths
from OpenDrive.client_side import file_changes_json as client_json


def full_synchronize() -> None:
    """Starts a sync process, where changes from server and client are merged."""
    server_changes = _get_server_changes()
    client_changes = _get_client_changes()
    server_actions, client_actions, conflicts = _merge_changes(server_changes, client_changes)
    _execute_server_actions(server_actions)
    _execute_client_actions(client_actions)


def _get_server_changes() -> dict:
    dest_path = os.path.join(client_paths.LOCAL_CLIENT_DATA, "server_changes.json")
    changes_file = server.get_changes(dest_path)
    with open(changes_file.dst_path, "r") as file:
        return json.load(file)


def _get_client_changes() -> dict:
    return client_json.get_all_data()


def _merge_changes(server_changes: dict, client_changes: dict) -> tuple:
    """TODO: pop items from the changes dicts, till both dicts are empty. All actions are instead distributed to the
    proper lists/dicts?"""
    needed_client_actions = []
    needed_server_actions = []
    conflicts = []

    while len(client_changes.keys()) > 0:
        folder_path, client_folder = client_changes.popitem()
        server_path = client_folder["server_folder_path"]
        server_folder = server_changes.pop(server_path)
        server_folder_changes = server_folder["changes"]
        client_folder_changes = client_folder["changes"]
        server_actions, client_actions, new_conflicts = _merge_folder_changes(server_folder_changes,
                                                                              client_folder_changes)
        needed_server_actions.append(server_actions)
        needed_client_actions.append(client_actions)
        conflicts.append(new_conflicts)

    return needed_server_actions, needed_client_actions, conflicts


def _merge_folder_changes(server_changes: dict, client_changes: dict) -> tuple:
    needed_client_actions = []
    needed_server_actions = []
    conflicts = []

    while len(client_changes.keys()) > 0:
        client_path, client_file = client_changes.popitem()
        if client_path in server_changes.keys():
            server_file = server_changes.pop(client_path)
        else:
            server_file = None

        server_actions, client_actions, new_conflicts = _merge_file_changes(client_file, server_file)
        needed_server_actions.append(server_actions)
        needed_client_actions.append(client_actions)
        conflicts.append(new_conflicts)

    while len(server_changes.keys()) > 0:
        server_path, server_file = server_changes.popitem()
        if server_path in client_changes.keys():
            client_file = client_changes.pop(server_path)
        else:
            client_file = None

        server_actions, client_actions, new_conflicts = _merge_file_changes(client_file, server_file)
        needed_server_actions.append(server_actions)
        needed_client_actions.append(client_actions)
        conflicts.append(new_conflicts)

    return needed_server_actions, needed_client_actions, conflicts


def _merge_file_changes(server_file: Optional[dict], client_file: Optional[dict]):
    needed_client_actions = []
    needed_server_actions = []
    conflicts = []

    return needed_server_actions, needed_client_actions, conflicts


def _execute_client_actions(client_actions) -> None:
    pass


def _execute_server_actions(server_actions) -> None:
    pass
