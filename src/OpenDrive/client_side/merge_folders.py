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


def merge_two_folders(folder_1_content: dict, folder_2_content: dict, merge_method: int):
    """Merges two folders content. Returns actions for both folders.
    """


def _take_1(folder_1_content: dict, folder_2_content: dict) -> Tuple[List[SyncAction], List[SyncAction]]:
    f1_actions = []
    f2_actions = []
    for dir_name, sub_dirnames, files in walk_directories(folder_2_content):
        action = c_syc.create_action()


class MergeMethods(Enum):
    TAKE_1 = _take_1  # Clear 2 and copy 1 into it
    TAKE_2 = auto()  # Clear 1 and copy 2 into it
    COMPLETE_BOTH = auto()  # Copies missing files at both sides
    CONFLICTS = auto()  # MERGE_COMPLETE_BOTH + create conflicts for files, that exists on both sides
    PRIORITIZE_1 = auto()  # MERGE_COMPLETE_BOTH + files that exists at both sides are taken from 1
    PRIORITIZE_2 = auto()  # MERGE_COMPLETE_BOTH + files that exists at both sides are taken from 2
    PRIORITIZE_LATEST = auto()  # MERGE_COMPLETE_BOTH + files that exists at both sides, the latest changed is taken


def walk_directories(dir_content: dict):
    """Directory tree generator.

    For each directory in the directory tree, yields a 3-tuple

        folder_name, dir_names, files (Tuple[filename, timestamp])
    """
    folder_name = dir_content["folder_name"]
    dir_names = [f["folder_name"] for f in dir_content["folders"]]
    files = [(f["file_name"], f["modified_timestamp"]) for f in dir_content["files"]]
    yield folder_name, dir_names, files

    for folder in dir_content["folders"]:
        yield from walk_directories(folder)
