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
import time
import json
import os
import typing
from typing import List
import copy

from OpenDrive.general.paths import NormalizedPath
from OpenDrive.general.file_exchanges import SyncAction
from OpenDrive.general.od_logging import logger_file_system

__all__ = ["init_file", "get_folder_entry", "add_change_entry", "remove_change_entry"]


ActionType = typing.NewType("ActionType", typing.Tuple[str, int])

ACTION_PULL = ActionType(("pull", 1 << 0))
ACTION_MOVE = ActionType(("move", 1 << 1))
ACTION_DELETE = ActionType(("delete", 1 << 2))
ACTION_MKDIR = ActionType(("mkdir", 1 << 3))


def init_file(file_path: str, empty: bool = False) -> None:
    if os.path.isfile(file_path):
        if empty:
            with open(file_path, "w+") as file:
                all_folders = {}
                json.dump(all_folders, file)
                logger_file_system.info(f"Empty changes file: {file_path}")
        else:
            logger_file_system.debug(f"Changes file already exists and is not changed: {file_path}")
    else:
        folder_path = os.path.split(file_path)[0]
        os.makedirs(folder_path, exist_ok=True)
        with open(file_path, "w+") as file:
            all_folders = {}
            json.dump(all_folders, file)
            logger_file_system.info(f"Created empty changes file: {file_path}")


def get_folder_entry(abs_folder_path: NormalizedPath, data: dict = None) -> dict:
    if data is None:
        data = _get_json_data()
    return data[abs_folder_path]


def add_change_entry(abs_folder_path: NormalizedPath, rel_entry_path: NormalizedPath, action: ActionType,
                     is_directory: bool = False, new_file_path: NormalizedPath = None) -> None:
    """rel_entry_path: key value in changes dict. create, delete -> current_path // move -> old_path"""
    data = _get_json_data()
    folder = get_folder_entry(abs_folder_path, data)
    changes = folder["changes"]
    if rel_entry_path in changes.keys():
        _update_existing_change_entry(changes, changes[rel_entry_path], rel_entry_path, action, is_directory,
                                      new_file_path)
    else:
        _add_new_change_entry(changes, rel_entry_path, action, is_directory, new_file_path)
    _set_json_data(data)


def remove_folder(folder_path: NormalizedPath, non_exists_ok=True):
    data = _get_json_data()
    try:
        data.pop(folder_path)
        _set_json_data(data)
    except KeyError:
        if not non_exists_ok:
            raise KeyError(f"Folder {folder_path} is not in json file!")


def remove_change_entry(abs_folder_path: NormalizedPath, rel_entry_path: NormalizedPath) -> None:
    data = _get_json_data()
    folder = get_folder_entry(abs_folder_path, data)
    changes: dict = folder["changes"]
    changes.pop(rel_entry_path)
    _set_json_data(data)


def can_folder_be_added(abs_folder_path: NormalizedPath) -> bool:
    """If new folder is not nested in any existing folder or would wrap around an existing folder, it can be added."""
    all_synced_folders = get_all_synced_folders_paths()
    return len([1 for existing_folder in all_synced_folders if abs_folder_path in existing_folder or existing_folder
                in abs_folder_path]) == 0


def _get_json_data() -> dict:
    raise NotImplemented


def _set_json_data(data: dict):
    raise NotImplemented


def _update_existing_change_entry(changes: dict, existing_entry: dict, rel_entry_path: NormalizedPath,
                                  action: ActionType, is_directory: bool = False, new_file_path: NormalizedPath = None):
    existing_entry["timestamp"] = get_current_timestamp()
    existing_entry["is_directory"] = is_directory
    if action == ACTION_MOVE:
        if existing_entry["action"] == ACTION_PULL[0]:
            _add_new_change_entry(changes, new_file_path, ACTION_PULL, is_directory)
            changes.pop(rel_entry_path)
            _add_new_change_entry(changes, rel_entry_path, ACTION_DELETE, is_directory)
        else:
            if existing_entry["rel_old_file_path"] is None:
                existing_entry["rel_old_file_path"] = rel_entry_path
            else:
                pass    # keep old old_file_path, because this is the name at the remote
            changes[new_file_path] = changes.pop(rel_entry_path)  # update rel_path key
    else:   # pull, delete
        if existing_entry["action"] == ACTION_MOVE[0]:
            changes.pop(rel_entry_path)
            _add_new_change_entry(changes, rel_entry_path, ACTION_PULL, is_directory)
            _add_new_change_entry(changes, existing_entry["rel_old_file_path"], ACTION_DELETE, is_directory)
        else:
            existing_entry["action"] = action[0]


def get_all_synced_folders_paths() -> List[NormalizedPath]:
    data = _get_json_data()
    return [folder_path for folder_path in data.keys()]


def _add_new_change_entry(changes: dict, rel_entry_path: NormalizedPath, action: ActionType,
                          is_directory: bool = False, new_file_path: NormalizedPath = None) -> None:
    entry = {"action": action[0],
             "timestamp": get_current_timestamp(),
             "is_directory": is_directory,
             "rel_old_file_path": None}
    if action == ACTION_MOVE:
        current_path = new_file_path
        entry["rel_old_file_path"] = rel_entry_path
    else:
        current_path = rel_entry_path
    changes[current_path] = entry


def remove_handled_changes(timestamp: float) -> None:
    """Possible issue: When file is changed, while this method is executed. The change may be overwritten."""
    data = _get_json_data()
    for folder_path, folder in data.items():
        idx = 0
        changes: typing.Dict[str] = folder["changes"]
        changes_copy: typing.Dict[str] = copy.deepcopy(changes)
        for k in changes.keys():
            change = changes_copy[k]
            if change["timestamp"] < timestamp:
                changes_copy.pop(k)
            else:
                idx += 1
        folder["changes"] = changes_copy

    _set_json_data(data)


def get_current_timestamp() -> float:
    return time.time()
