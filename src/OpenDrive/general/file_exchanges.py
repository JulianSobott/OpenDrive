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

import pynetworking as net


def get_file(abs_file_src_path: str, abs_file_dest_path: str) -> net.File:
    if os.path.isfile(abs_file_src_path):
        return net.File(abs_file_src_path, abs_file_dest_path)
    else:
        raise FileNotFoundError


class Action:

    def __init__(self, abs_local_path: str):
        self.abs_local_path = abs_local_path

    def run(self):
        raise NotImplementedError


def move_file(abs_src_path: str, abs_dest_path: str):
    """Folders that don't exist are created"""
    os.makedirs(os.path.split(abs_dest_path)[0], exist_ok=True)
    shutil.move(abs_src_path, abs_dest_path)


def remove_file(abs_src_path: str):
    os.remove(abs_src_path)