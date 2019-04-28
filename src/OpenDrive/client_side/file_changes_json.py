"""
:module: OpenDrive.client_side.file_changes_json
:synopsis: Read and edit the json file, that stores folders and changes
:author: Julian Sobott

public functions
-----------------

.. autofunction:: init_file
.. autofunction:: add_folder
.. autofunction:: remove_folder
.. autofunction:: get_all_synced_folders_paths
.. autofunction:: get_folder_entry
.. autofunction:: set_include_regexes
.. autofunction:: set_exclude_regexes

private functions
------------------

.. autofunction:: _can_folder_be_added
.. autofunction:: _get_json_data
.. autofunction:: _set_json_data
.. autofunction:: _create_folder_entry

"""
import datetime
import json
import os
import time
import typing
from typing import List, Union, TypeVar

from OpenDrive.client_side import paths as client_paths
from OpenDrive.general.paths import NormalizedPath

__all__ = ["init_file", "add_folder", "remove_folder", "get_all_synced_folders_paths","get_folder_entry",
           "set_include_regexes", "set_exclude_regexes"]


CHANGE_MOVED = ("moved", 1<<0)
CHANGE_CREATED = ("created", 1 << 0)
CHANGE_MODIFIED = ("modified", 1 << 0)
CHANGE_DELETED = ("deleted", 1 << 0)

ACTION_PULL = ("pull", 1 << 0)
ACTION_MOVE = ("move", 1 << 0)
ACTION_DELETE = ("delete", 1 << 0)

ChangeType = typing.NewType("ChangeType", tuple)
ActionType = typing.NewType("ActionType", tuple)


def init_file() -> None:
    os.makedirs(client_paths.LOCAL_CLIENT_DATA, exist_ok=True)
    with open(client_paths.LOCAL_JSON_PATH, "w+") as file:
        all_folders = []
        json.dump(all_folders, file)


def add_folder(abs_folder_path: NormalizedPath, include_regexes: List[str], exclude_regexes: List[str]) -> bool:
    if not _can_folder_be_added(abs_folder_path):
        return False
    data = _get_json_data()
    new_folder_entry = _create_folder_entry(abs_folder_path, include_regexes, exclude_regexes)
    data.append(new_folder_entry)
    _set_json_data(data)
    return True


def remove_folder(abs_folder_path: NormalizedPath, non_exists_ok=True):
    data = _get_json_data()
    for idx, entry in enumerate(data):
        if abs_folder_path == entry["folder_path"]:
            data.pop(idx)
            _set_json_data(data)
            return
    if not non_exists_ok:
        raise KeyError(f"Folder {abs_folder_path} is not in json file!")


def get_all_synced_folders_paths() -> List[NormalizedPath]:
    data = _get_json_data()
    return [folder_entry["folder_path"] for folder_entry in data]


def get_all_synced_folders() -> List:
    return _get_json_data()


def set_include_regexes(abs_folder_path: NormalizedPath, include_regexes: List[str]) -> None:
    _set_folder_attribute(abs_folder_path, "include_regexes", include_regexes)


def set_exclude_regexes(abs_folder_path: NormalizedPath, exclude_regexes: List[str]) -> None:
    _set_folder_attribute(abs_folder_path, "exclude_regexes", exclude_regexes)


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


def _can_folder_be_added(abs_folder_path: NormalizedPath) -> bool:
    """If new folder is not nested in any existing folder or would wrap around an existing folder, it can be added."""
    all_synced_folders = get_all_synced_folders_paths()
    return len([1 for existing_folder in all_synced_folders if abs_folder_path in existing_folder or existing_folder
                in abs_folder_path]) == 0


def _get_json_data() -> List:
    with open(client_paths.LOCAL_JSON_PATH, "r") as file:
        return json.load(file)


def _set_json_data(data: List):
    with open(client_paths.LOCAL_JSON_PATH, "w") as file:
        return json.dump(data, file)


def _create_folder_entry(abs_folder_path: NormalizedPath, include_regexes: List[str], exclude_regexes: List[str]) -> \
        dict:
    return {"folder_path": abs_folder_path,
            "include_regexes": include_regexes,
            "exclude_regexes": exclude_regexes,
            "changes": [],
            }


def _set_folder_attribute(abs_folder_path: NormalizedPath, key: str, value: Union[str, list, int, dict]) -> None:
    data = _get_json_data()
    for entry in data:
        if abs_folder_path == entry["folder_path"]:
            entry[key] = value
            break
    _set_json_data(data)


def _update_existing_change_entry(existing_entry: dict, rel_entry_path: NormalizedPath, change_type: ChangeType,
                                  action: ActionType, is_directory: bool = False, new_file_path: NormalizedPath = None):
    existing_entry["last_change_time_stamp"] = str(datetime.datetime.now())
    existing_entry["is_directory"] = is_directory
    if action == ACTION_MOVE:
        existing_entry["new_file_path"] = new_file_path
        existing_entry["old_file_path"] = rel_entry_path
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
