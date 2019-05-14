"""
:module: OpenDrive.general.file_exchanges
:synopsis: Send and receive files over the network
:author: Julian Sobott
public functions
-----------------
.. autofunction:: get_file

private functions
------------------
"""
import os
import shutil
from typing import NewType

import pynetworking as net


def get_file(abs_file_src_path: str, abs_file_dest_path: str) -> net.File:
    if os.path.isfile(abs_file_src_path):
        return net.File(abs_file_src_path, abs_file_dest_path)
    else:
        raise FileNotFoundError(abs_file_src_path)


class Action:

    def __init__(self, abs_local_path: str):
        self.abs_local_path = abs_local_path

    def run(self):
        raise NotImplementedError


def move_file(src_path: str, dest_path: str, implicit=True):
    """"""
    if not implicit:
        """src_file must exist, dest_folder must exist, dest_file must not exist."""
        if not os.path.isfile(src_path):
            raise FileNotFoundError(src_path)
        dest_folder = os.path.split(dest_path)[0]
        if not os.path.exists(dest_folder):
            raise FileNotFoundError(f"Destination folder does not exist: {dest_folder}")
        if os.path.isfile(dest_path):
            raise FileExistsError(dest_path)
    shutil.move(src_path, dest_path)


def remove_file(abs_src_path: str, implicit=True):
    """For now just deletes the file. A backup system could be added later."""
    try:
        os.remove(abs_src_path)
    except FileNotFoundError as e:
        if not implicit:
            raise e


SyncAction = NewType("SyncAction", dict)