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
from typing import Tuple, List

from OpenDrive.general.file_exchanges import SyncAction
from OpenDrive.client_side import synchronization as c_syc
from OpenDrive.general import file_changes_json as gen_json
from OpenDrive.general.paths import NormalizedPath, normalize_path


def merge_two_folders(folder_1_content: dict, folder_2_content: dict, merge_method: int):
    """Merges two folders content. Returns actions for both folders.
    """


def _take_1(folder_1_content: dict, folder_2_content: dict) -> Tuple[List[SyncAction], List[SyncAction]]:
    f1_actions = []
    f2_actions = []
    f1_folder_name = folder_1_content["folder_name"]
    f2_folder_name = folder_2_content["folder_name"]

    f2_actions.append(c_syc.create_action(f2_folder_name, normalize_path(""), gen_json.ACTION_DELETE, True))
    f2_actions.append(c_syc.create_action(f2_folder_name, normalize_path(""), gen_json.ACTION_PULL, True))
    return f1_actions, f2_actions


def _take_2(folder_1_content: dict, folder_2_content: dict) -> Tuple[List[SyncAction], List[SyncAction]]:
    return _take_1(folder_2_content, folder_1_content)


class MergeMethods(Enum):
    TAKE_1 = _take_1  # Clear 2 and copy 1 into it
    TAKE_2 = _take_2  # Clear 1 and copy 2 into it
    COMPLETE_BOTH = auto()  # Copies missing files at both sides
    CONFLICTS = auto()  # MERGE_COMPLETE_BOTH + create conflicts for files, that exists on both sides
    PRIORITIZE_1 = auto()  # MERGE_COMPLETE_BOTH + files that exists at both sides are taken from 1
    PRIORITIZE_2 = auto()  # MERGE_COMPLETE_BOTH + files that exists at both sides are taken from 2
    PRIORITIZE_LATEST = auto()  # MERGE_COMPLETE_BOTH + files that exists at both sides, the latest changed is taken


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
