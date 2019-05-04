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
.. autofunction:: add_change_entry
.. autofunction:: remove_change_entry

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
from OpenDrive.general import file_changes_json as gen_json

__all__ = ["init_file", "add_folder", "remove_folder", "get_folder_entry",
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


def init_file(empty: bool = False) -> None:
    return gen_json.init_file(client_paths.LOCAL_JSON_PATH, empty)


def add_folder(abs_folder_path: NormalizedPath, include_regexes: List[str], exclude_regexes: List[str]) -> bool:
    if not gen_json.can_folder_be_added(abs_folder_path):
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


def get_all_synced_folders() -> List:
    return _get_json_data()


def set_include_regexes(abs_folder_path: NormalizedPath, include_regexes: List[str]) -> None:
    _set_folder_attribute(abs_folder_path, "include_regexes", include_regexes)


def set_exclude_regexes(abs_folder_path: NormalizedPath, exclude_regexes: List[str]) -> None:
    _set_folder_attribute(abs_folder_path, "exclude_regexes", exclude_regexes)


def add_change_entry(abs_folder_path: NormalizedPath, rel_entry_path: NormalizedPath, change_type: ChangeType,
                     action: ActionType, is_directory: bool = False, new_file_path: NormalizedPath = None) -> None:
    return gen_json.add_change_entry(abs_folder_path, rel_entry_path, change_type, action, is_directory, new_file_path)


def remove_change_entry(abs_folder_path: NormalizedPath, rel_entry_path: NormalizedPath) -> None:
    return gen_json.remove_change_entry(abs_folder_path, rel_entry_path)


def get_folder_entry(abs_folder_path: NormalizedPath):
    return gen_json.get_folder_entry(abs_folder_path)


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


gen_json._set_json_data = _set_json_data
gen_json._get_json_data = _get_json_data
