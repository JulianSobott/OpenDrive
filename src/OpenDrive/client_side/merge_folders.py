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

.. autofunction:: _take_1
.. autofunction:: _take_2

"""
from enum import auto
from typing import Tuple, List, Callable, NewType

from OpenDrive.general.file_exchanges import SyncAction
from OpenDrive.general import merge_folders as gen_merge_folders
from OpenDrive.general import file_changes_json as gen_json
from OpenDrive.general.paths import normalize_path
from OpenDrive.client_side import synchronization as c_syc
from OpenDrive.client_side import synchronization as client_sync
from OpenDrive.client_side import interface
from OpenDrive import net_interface

MergeMethod = NewType("MergeMethod", Callable)


def merge_folders(abs_local_path: str, remote_name: str, merge_method: MergeMethod) -> 'interface.Status':
    try:
        server_content = net_interface.server.generate_content_of_folder(remote_name)
    except FileNotFoundError:
        return interface.Status.fail(f"Server folder ({remote_name}) does not exist!")
    try:
        client_content = gen_merge_folders.generate_content_of_folder(abs_local_path)
    except FileNotFoundError:
        return interface.Status.fail(f"Client folder ({abs_local_path}) does not exist!")
    client_actions,  server_actions = merge_two_folders(client_content, server_content, merge_method)
    net_interface.server.execute_actions(server_actions)
    client_sync.execute_client_actions(client_actions)
    return interface.Status.success("Successfully merged folders")


def merge_two_folders(folder_1_content: dict, folder_2_content: dict, merge_method: MergeMethod):
    """Merges two folders content. Returns actions for both folders. The contents are generated by
    :func:`generate_content_of_folder`
    """
    return merge_method(folder_1_content, folder_2_content)


def _take_1(folder_1_content: dict, folder_2_content: dict) -> Tuple[List[SyncAction], List[SyncAction]]:
    """Some docs"""
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
    TAKE_1: MergeMethod = MergeMethod(_take_1)  #: Clear 2 and copy 1 into it
    TAKE_2 = MergeMethod(_take_2)  #: Clear 1 and copy 2 into it
    COMPLETE_BOTH = auto()  #: Copies missing files at both sides
    CONFLICTS: Callable = auto()  #: MERGE_COMPLETE_BOTH + create conflicts for files, that exists on both sides
    PRIORITIZE_1: Callable = auto()  #: MERGE_COMPLETE_BOTH + files that exists at both sides are taken from 1
    PRIORITIZE_2: Callable = auto()  #: MERGE_COMPLETE_BOTH + files that exists at both sides are taken from 2
    #: MERGE_COMPLETE_BOTH + files that exists at both sides, the latest changed is taken
    PRIORITIZE_LATEST: Callable = auto()
    DEFAULT = TAKE_1


