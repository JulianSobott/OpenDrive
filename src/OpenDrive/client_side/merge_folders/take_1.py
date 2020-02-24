"""
:module: OpenDrive.client_side.merge_folders.take_1
:synopsis: Make a complete copy of folder_1 in folder_2
:author: Julian Sobott


public functions
----------------

.. autofunction:: take_1

"""
from typing import Tuple, List

from OpenDrive.general.file_exchanges import SyncAction
from OpenDrive.general import file_changes_json as gen_json
from OpenDrive.general.paths import normalize_path, NormalizedPath
from OpenDrive.client_side import synchronization as c_syc

NAME = "Take folder 1"
DESCRIPTION = "Make a complete copy of folder_1 in folder_2 "


def take_1(folder_1_content: dict, folder_2_content: dict) -> Tuple[List[SyncAction], List[SyncAction]]:
    f1_actions = []
    f2_actions = []
    f1_folder_name = folder_1_content["folder_name"]
    f2_folder_name = folder_2_content["folder_name"]

    f2_actions.append(c_syc.create_action(f2_folder_name, NormalizedPath(""), gen_json.ACTION_DELETE, True))
    f2_actions.append(c_syc.create_action(f2_folder_name, NormalizedPath(""), gen_json.ACTION_PULL, True,
                                          remote_abs_path=f1_folder_name))
    return f1_actions, f2_actions


method = take_1
