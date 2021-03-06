"""
:module: OpenDrive.client_side.file_changes_json
:synopsis: Read and edit the json file, that stores folders and changes
:author: Julian Sobott

public functions
-----------------

.. autofunction:: add_change_entry
.. autofunction:: add_folder
.. autofunction:: get_all_data
.. autofunction:: get_folder_entry
.. autofunction:: init_file
.. autofunction:: remove_change_entry
.. autofunction:: remove_folder
.. autofunction:: set_exclude_regexes
.. autofunction:: set_include_regexes


private functions
------------------

.. autofunction:: _create_folder_entry
.. autofunction:: _get_json_data
.. autofunction:: _override_gen_functions
.. autofunction:: _set_folder_attribute
.. autofunction:: _set_json_data

"""
import json
from typing import List, Union, Optional
from functools import wraps

from OpenDrive.client_side import paths as client_paths
from OpenDrive.general.paths import NormalizedPath
from OpenDrive.general import file_changes_json as gen_json


def _override_gen_functions(func):
    """Decorator to set the `set` and `get` functions calls in the general module."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        gen_json._set_json_data = _set_json_data
        gen_json._get_json_data = _get_json_data
        ret_value = func(*args, **kwargs)
        return ret_value

    return wrapper


@_override_gen_functions
def init_file(empty: bool = False) -> None:
    """

    :param empty: True: all content will be deleted. This is only useful for testing purposes
    :return: None
    """
    return gen_json.init_file(client_paths.LOCAL_JSON_PATH, empty)


@_override_gen_functions
def add_folder(abs_folder_path: NormalizedPath, include_regexes: List[str], exclude_regexes: List[str],
               server_folder_path: Optional[NormalizedPath] = None) -> bool:
    if not gen_json.can_folder_be_added(abs_folder_path):
        return False
    data = _get_json_data()
    new_folder_entry = _create_folder_entry(server_folder_path, include_regexes, exclude_regexes)
    data[abs_folder_path] = new_folder_entry
    _set_json_data(data)
    return True


@_override_gen_functions
def remove_folder(abs_folder_path: NormalizedPath, non_exists_ok=True):
    return gen_json.remove_folder(abs_folder_path, non_exists_ok)


@_override_gen_functions
def get_all_data() -> dict:
    """
    :returns:
        A dict of all synced folders and the changes data. The structure of the dict is documented in
        :doc:`file_changes_json`"""
    return _get_json_data()


@_override_gen_functions
def set_include_regexes(abs_folder_path: NormalizedPath, include_regexes: List[str]) -> None:
    _set_folder_attribute(abs_folder_path, "include_regexes", include_regexes)


@_override_gen_functions
def set_exclude_regexes(abs_folder_path: NormalizedPath, exclude_regexes: List[str]) -> None:
    _set_folder_attribute(abs_folder_path, "exclude_regexes", exclude_regexes)


@_override_gen_functions
def add_change_entry(abs_folder_path: NormalizedPath, rel_entry_path: NormalizedPath,
                     action: gen_json.ActionType, is_directory: bool = False, new_file_path: NormalizedPath = None) \
        -> None:
    return gen_json.add_change_entry(abs_folder_path, rel_entry_path, action, is_directory, new_file_path)


@_override_gen_functions
def remove_change_entry(abs_folder_path: NormalizedPath, rel_entry_path: NormalizedPath) -> None:
    return gen_json.remove_change_entry(abs_folder_path, rel_entry_path)


@_override_gen_functions
def get_folder_entry(abs_folder_path: NormalizedPath):
    return gen_json.get_folder_entry(abs_folder_path)


def _get_json_data() -> dict:
    with open(client_paths.LOCAL_JSON_PATH, "r") as file:
        return json.load(file)


def _set_json_data(data: dict):
    with open(client_paths.LOCAL_JSON_PATH, "w") as file:
        return json.dump(data, file, indent=4)


@_override_gen_functions
def _create_folder_entry(server_folder_path: NormalizedPath, include_regexes: List[str], exclude_regexes: List[str]) \
        -> dict:
    return {"server_folder_path": server_folder_path,
            "include_regexes": include_regexes,
            "exclude_regexes": exclude_regexes,
            "changes": {},
            }


@_override_gen_functions
def _set_folder_attribute(abs_folder_path: NormalizedPath, key: str, value: Union[str, list, int, dict]) -> None:
    data = _get_json_data()
    entry = data[abs_folder_path]
    entry[key] = value
    _set_json_data(data)
