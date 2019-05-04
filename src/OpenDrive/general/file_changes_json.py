"""
:module: OpenDrive.general.file_changes_json
:synopsis: Read and edit the json file, that stores and changes
:author: Julian Sobott

public functions
-----------------

.. autofunction:: init_file
.. autofunction:: get_folder_entry
.. autofunction:: add_change_entry
.. autofunction:: remove_change_entry


private functions
------------------

.. autofunction:: _get_json_data
.. autofunction:: _set_json_data
.. autofunction:: _update_existing_change_entry
.. autofunction:: _add_new_change_entry

"""
import datetime
import json
import os
import time
import typing
from typing import List, Union, TypeVar

from OpenDrive.client_side import paths as client_paths
from OpenDrive.general.paths import NormalizedPath

__all__ = ["init_file", "get_folder_entry", "add_change_entry", "remove_change_entry"]


CHANGE_MOVED = ("moved", 1<<0)
CHANGE_CREATED = ("created", 1 << 0)
CHANGE_MODIFIED = ("modified", 1 << 0)
CHANGE_DELETED = ("deleted", 1 << 0)

ACTION_PULL = ("pull", 1 << 0)
ACTION_MOVE = ("move", 1 << 0)
ACTION_DELETE = ("delete", 1 << 0)

ChangeType = typing.NewType("ChangeType", tuple)
ActionType = typing.NewType("ActionType", tuple)


def init_file(file_path: str, empty: bool = False) -> None:
    if os.path.isfile(file_path):
        if empty:
            with open(file_path, "w+") as file:
                all_folders = []
                json.dump(all_folders, file)
    folder_path = os.path.split(file_path)[0]
    os.makedirs(folder_path, exist_ok=True)
    with open(file_path, "w+") as file:
        all_folders = []
        json.dump(all_folders, file)


def get_folder_entry(abs_folder_path: NormalizedPath, data: list = None) -> dict:
    if data is None:
        data = _get_json_data()
    for entry in data:
        if abs_folder_path == entry["folder_path"]:
            return entry


def add_change_entry(abs_folder_path: NormalizedPath, rel_entry_path: NormalizedPath, change_type: ChangeType,
                     action: ActionType, is_directory: bool = False, new_file_path: NormalizedPath = None) -> None:
    data = _get_json_data()
    folder = get_folder_entry(abs_folder_path, data)
    changes = folder["changes"]
    for entry in changes:
        if entry["new_file_path"] == rel_entry_path:
            _update_existing_change_entry(entry, rel_entry_path, change_type, action, is_directory, new_file_path)
            _set_json_data(data)
            return
    _add_new_change_entry(changes, rel_entry_path, change_type, action, is_directory, new_file_path)
    _set_json_data(data)


def remove_change_entry(abs_folder_path: NormalizedPath, rel_entry_path: NormalizedPath) -> None:
    data = _get_json_data()
    folder = get_folder_entry(abs_folder_path, data)
    changes: list = folder["changes"]
    for idx, entry in enumerate(changes):
        if entry["new_file_path"] == rel_entry_path:
            changes.pop(idx)
            _set_json_data(data)


def _get_json_data() -> List:
    raise NotImplemented


def _set_json_data(data: List):
    raise NotImplemented


def _update_existing_change_entry(existing_entry: dict, rel_entry_path: NormalizedPath, change_type: ChangeType,
                                  action: ActionType, is_directory: bool = False, new_file_path: NormalizedPath = None):
    existing_entry["last_change_time_stamp"] = str(datetime.datetime.now())
    existing_entry["is_directory"] = is_directory
    if action == ACTION_MOVE:
        existing_entry["new_file_path"] = new_file_path
        if "old_file_path" not in existing_entry.keys():
            existing_entry["old_file_path"] = rel_entry_path
        else:
            pass    # keep old old_file_path, because this is the name at the remote
    else:
        existing_entry["new_file_path"] = rel_entry_path

    if action == ACTION_MOVE and existing_entry["necessary_action"] == ACTION_PULL[0]:
        existing_entry["necessary_action"] = ACTION_PULL[0]
    else:
        existing_entry["necessary_action"] = action[0]

    if change_type == CHANGE_CREATED or change_type == CHANGE_DELETED:
        existing_entry["changes"] = [change_type[0]]
    if change_type == CHANGE_MODIFIED or change_type == CHANGE_MODIFIED:
        existing_entry["changes"].append(change_type[0])


def _add_new_change_entry(changes: list, rel_entry_path: NormalizedPath, change_type: ChangeType,
                          action: ActionType, is_directory: bool = False, new_file_path: NormalizedPath = None) -> None:
    entry = {}
    if action == ACTION_MOVE:
        entry["new_file_path"] = new_file_path
        entry["old_file_path"] = rel_entry_path
    else:
        entry["new_file_path"] = rel_entry_path
    entry["last_change_time_stamp"] = str(datetime.datetime.now())
    entry["changes"] = [change_type[0]]
    entry["necessary_action"] = action[0]
    entry["is_directory"] = is_directory
    changes.append(entry)