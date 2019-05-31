"""
:module: OpenDrive.client_side.merge_folders.take_2
:synopsis: Make a complete copy of folder_2 in folder_1
:author: Julian Sobott


public functions
----------------

.. autofunction:: take_2

"""
from typing import Tuple, List

from OpenDrive.general.file_exchanges import SyncAction

from OpenDrive.client_side.merge_folders import take_1

NAME = "Take folder 2"
DESCRIPTION = "Make a complete copy of folder_2 in folder_1"


def take_2(folder_1_content: dict, folder_2_content: dict) -> Tuple[List[SyncAction], List[SyncAction]]:
    f1_actions, f2_actions = take_1.take_1(folder_2_content, folder_1_content)
    return f2_actions, f1_actions


method = take_2
