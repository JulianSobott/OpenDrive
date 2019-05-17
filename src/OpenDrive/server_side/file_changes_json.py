"""
:module: OpenDrive.server_side.file_changes_json
:synopsis: Handles the json changes file at the server
:author: Julian Sobott

Each device has its own changes file.
Filename: changes_{device_id}.json

In the changes are the changes stored, that needs to be synchronized. (Not the changes that occurred on that device.)

e.g. d1 creates a file. this file is uploaded to the server. in the changes file of all other devices is written:
created new file.


public functions
----------------

.. autofunction:: create_changes_file_for_new_device
.. autofunction:: get_file_name

private functions
-----------------


"""
import json
import os
from typing import List

import pynetworking as net

from OpenDrive.server_side import paths as server_paths
from OpenDrive.general import file_changes_json as gen_json
from OpenDrive.general.file_exchanges import SyncAction
from OpenDrive.general.paths import NormalizedPath
from OpenDrive import net_interface
from OpenDrive.general.file_changes_json import ActionType


def _override_gen_functions(func):
    def wrapper(*args, **kwargs):
        gen_json._set_json_data = _set_json_data
        gen_json._get_json_data = _get_json_data
        ret_value = func(*args, **kwargs)
        return ret_value

    return wrapper


@_override_gen_functions
def get_file_name(device_id: int):
    return f"changes_{device_id}.json"


@_override_gen_functions
def create_changes_file_for_new_device(user_id: int, device_id: int, empty: bool = False) -> None:
    file_path = _get_file_path(user_id, device_id)
    return gen_json.init_file(file_path, empty)


@_override_gen_functions
def add_folder(folder_name: str) -> bool:
    if not gen_json.can_folder_be_added(server_paths.NormalizedPath(folder_name)):
        return False
    data = _get_json_data()
    new_folder_entry = {"changes": {}}
    data[folder_name] = new_folder_entry
    _set_json_data(data)
    return True


@_override_gen_functions
def remove_folder(rel_folder_path: NormalizedPath, non_exists_ok=True):
    return gen_json.remove_folder(rel_folder_path, non_exists_ok)


@_override_gen_functions
def add_change_entry(abs_folder_path: NormalizedPath, rel_entry_path: NormalizedPath, action: gen_json.ActionType,
                     is_directory: bool = False, new_file_path: NormalizedPath = None) -> None:
    return gen_json.add_change_entry(abs_folder_path, rel_entry_path, action, is_directory, new_file_path)


@_override_gen_functions
def remove_change_entry(abs_folder_path: NormalizedPath, rel_entry_path: NormalizedPath) -> None:
    return gen_json.remove_change_entry(abs_folder_path, rel_entry_path)


def _get_json_data() -> dict:
    user: net_interface.ClientCommunicator = net.ClientManager().get()
    file_path = _get_file_path(user.user_id, user.device_id)
    with open(file_path, "r") as file:
        return json.load(file)


def _set_json_data(data: dict):
    user: net_interface.ClientCommunicator = net.ClientManager().get()
    file_path = _get_file_path(user.user_id, user.device_id)
    with open(file_path, "w") as file:
        return json.dump(data, file)


@_override_gen_functions
def _get_file_path(user_id: int, device_id: int) -> str:
    user_path = server_paths.get_users_root_folder(user_id)
    file_path = os.path.join(user_path, get_file_name(device_id))
    return file_path


@_override_gen_functions
def _has_folder(folder_path: NormalizedPath) -> bool:
    data = _get_json_data()
    return folder_path in data.keys()


def distribute_action(action: SyncAction, devices_ids: List[int]) -> None:
    for device_id in devices_ids:
        _get_file_path = lambda user_id, _: _get_file_path(user_id, device_id)
        if _has_folder(action["local_folder_path"]):
            if action["rel_old_file_path"] is None:
                rel_file_path = action["rel_file_path"]
                new_file_path = None
            else:
                rel_file_path = action["rel_old_file_path"]
                new_file_path = action["rel_file_path"]
            add_change_entry(action["local_folder_path"], rel_file_path, ActionType((action["action_type"], 0)),
                             action["is_directory"], new_file_path)
