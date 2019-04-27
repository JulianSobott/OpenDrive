"""
:module: OpenDrive.client_side.file_changes_json
:synopsis: Read and edit the json file, that stores folders and changes
:author: Julian Sobott

public functions
-----------------

.. autofunction:: init_file
.. autofunction:: add_folder
.. autofunction:: get_all_synced_folders_paths

private functions
------------------

.. autofunction:: _can_folder_be_added
.. autofunction:: _get_json_data
.. autofunction:: _set_json_data
.. autofunction:: _create_folder_entry

"""
import json
import os
from typing import List

from OpenDrive.client_side import paths as client_paths
from OpenDrive.general.paths import NormalizedPath

__all__ = ["init_file"]


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


def get_all_synced_folders_paths() -> List[NormalizedPath]:
    data = _get_json_data()
    return [folder_entry["folder_path"] for folder_entry in data]


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
