"""
:module: OpenDrive.client_side.merge_folders
:synopsis: Merge files and of two folders, based on a merge method.
:author: Julian Sobott

This is needed, when a folder is synced with an existing folder.

Dict structure for content of a folder:

    Folder:
        "folder_name": top_folder_name,
        "files": List[Dict["filename": str, "modified_timestamp": str]
        "folders": List[Folder]

    e.g.

    {
    "folder_name": "top",
    "files": [{"file_name": "test.txt", "modified_timestamp": 1234}, ...],
    "folders": [{"folder_name": ...},{...}, ...]
    }

public classes
---------------

.. autoclass:: MergeMethods
    :members:


public functions
----------------

.. autofunction:: merge_two_folders

private functions
-----------------

.. autofunction:: walk_directories

"""
import os
from enum import Enum, auto
from typing import Tuple, List, Callable

from OpenDrive.general.file_exchanges import SyncAction
from OpenDrive.client_side import synchronization as c_syc
from OpenDrive.general import file_changes_json as gen_json
from OpenDrive.general.paths import NormalizedPath, normalize_path


def merge_two_folders(folder_1_content: dict, folder_2_content: dict, merge_method: Callable):
    """Merges two folders content. Returns actions for both folders.
    """
    return merge_method(folder_1_content, folder_2_content)


def _take_1(folder_1_content: dict, folder_2_content: dict) -> Tuple[List[SyncAction], List[SyncAction]]:
    f1_actions = []
    f2_actions = []
    f1_folder_name = folder_1_content["folder_name"]
    f2_folder_name = folder_2_content["folder_name"]

    f2_actions.append(c_syc.create_action(f2_folder_name, normalize_path(""), gen_json.ACTION_DELETE, True))
    f2_actions.append(c_syc.create_action(f2_folder_name, normalize_path(""), gen_json.ACTION_PULL, True,
                                          remote_abs_path=f1_folder_name))
    return f1_actions, f2_actions


def _take_2(folder_1_content: dict, folder_2_content: dict) -> Tuple[List[SyncAction], List[SyncAction]]:
    return _take_1(folder_2_content, folder_1_content)


class MergeMethods:
    TAKE_1: Callable = _take_1  # Clear 2 and copy 1 into it
    TAKE_2: Callable = _take_2  # Clear 1 and copy 2 into it
    COMPLETE_BOTH: Callable = auto()  # Copies missing files at both sides
    CONFLICTS: Callable = auto()  # MERGE_COMPLETE_BOTH + create conflicts for files, that exists on both sides
    PRIORITIZE_1: Callable = auto()  # MERGE_COMPLETE_BOTH + files that exists at both sides are taken from 1
    PRIORITIZE_2: Callable = auto()  # MERGE_COMPLETE_BOTH + files that exists at both sides are taken from 2
    PRIORITIZE_LATEST: Callable = auto()  # MERGE_COMPLETE_BOTH + files that exists at both sides, the latest changed is taken


def walk_directories(dir_content: dict, parent_path: NormalizedPath):
    """Directory tree generator.

    For each directory in the directory tree, yields a 3-tuple

        parent_path, dir_path, files (Tuple[filename, timestamp])

        path of file: parent_path + dir_path + file_name
    """
    folder_name = dir_content["folder_name"]
    files = [(f["file_name"], f["modified_timestamp"]) for f in dir_content["files"]]
    yield parent_path, folder_name, files

    for folder in dir_content["folders"]:
        yield from walk_directories(folder, normalize_path(parent_path, dir_content["folder_name"]))


def generate_content_of_folder(abs_folder_path: str) -> dict:
    """
    :param abs_folder_path:
    :return: dict with following structure

        Folder:
            "folder_name": top_folder_name,
            "files": List[Dict["filename": str, "modified_timestamp": str]
            "folders": List[Folder]
    """
    return _recursive_generate_content_of_folder(abs_folder_path, abs_folder_path)


def _recursive_generate_content_of_folder(abs_folder_path: str, folder_name: str):
    content = {
        "folder_name": folder_name,
        "files": [],
        "folders": []
    }
    _, dir_list, file_list = next(os.walk(abs_folder_path))
    for file in file_list:
        file_path = os.path.join(abs_folder_path, file)
        content["files"].append({"file_name": file, "modified_timestamp": os.path.getmtime(file_path)})
    for dir_name in dir_list:
        abs_path = os.path.join(abs_folder_path, dir_name)
        content["folders"].append(_recursive_generate_content_of_folder(abs_path, dir_name))
    return content


if __name__ == '__main__':
    print(MergeMethods.TAKE_1)


