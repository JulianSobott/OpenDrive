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

from OpenDrive.net_interface import server
from OpenDrive.client_side import paths as client_paths


def full_synchronize() -> None:
    """Starts a sync process, where changes from server and client are merged."""
    server_changes = _get_server_changes()
    client_changes = _get_client_changes()
    server_actions, client_actions, conflicts = _merge_changes(server_changes, client_changes)
    _execute_server_actions(server_actions)
    _execute_client_actions(client_actions)


def _get_server_changes() -> list:
    changes_file = server.get_changes(client_paths.LOCAL_CLIENT_DATA)
    with open(changes_file, "r") as file:
        return json.load(file)


def _get_client_changes() -> list:
    pass


def _merge_changes(server_changes: list, client_changes: list) -> tuple:
    pass


def _execute_client_actions(client_actions) -> None:
    pass


def _execute_server_actions(server_actions) -> None:
    pass
