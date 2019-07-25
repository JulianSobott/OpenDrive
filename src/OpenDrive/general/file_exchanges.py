"""
:module: OpenDrive.general.file_exchanges
:synopsis: Exchange, move and delete files.
:author: Julian Sobott

public functions
-----------------

.. autofunction:: get_file
.. autofunction:: move
.. autofunction:: make_dirs
.. autofunction:: remove_file

"""
import os
import shutil
from typing import NewType, Callable
import pynetworking as net

from OpenDrive.general import paths as gen_paths


def get_file(abs_file_src_path: str, abs_file_dest_path: str) -> net.File:
    if os.path.isfile(abs_file_src_path):
        return net.File(abs_file_src_path, abs_file_dest_path)
    else:
        raise FileNotFoundError(abs_file_src_path)


def get_dir(abs_src_path: str, abs_dest_path: str, pull_file_func: Callable, make_dirs_func: Callable) -> None:
    """Every file inside the abs_src_path is copied to the proper abs_dest_path."""
    for dirpath, dirnames, filenames in os.walk(abs_src_path):
        rel_folder_name = os.path.relpath(dirpath, abs_src_path)
        for dir in dirnames:
            dest_path = gen_paths.normalize_path(abs_dest_path, rel_folder_name, dir)
            make_dirs_func(dest_path)
        for file in filenames:
            abs_src_file_path = gen_paths.normalize_path(dirpath, file)
            abs_dest_file_path = gen_paths.normalize_path(abs_dest_path, rel_folder_name, file)
            pull_file_func(abs_src_file_path, abs_dest_file_path)


def move(src_path: str, dest_path: str, implicit=True):
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


def make_dirs(abs_path: str, exist_ok: bool = True):
    os.makedirs(abs_path, exist_ok=exist_ok)


def remove_file(abs_src_path: str, implicit=True):
    """For now just deletes the file. A backup system could be added later."""
    try:
        os.remove(abs_src_path)
    except FileNotFoundError as e:
        if not implicit:
            raise e


def remove_dir(abs_path: str, only_empty: bool = False):
    if not os.path.exists(abs_path):
        raise FileNotFoundError(f"Cannot remove non existing directory! {abs_path}")
    if only_empty and len(os.listdir(abs_path)) > 0:
        raise FileExistsError(f"Directory is not empty! {abs_path}")
    shutil.rmtree(abs_path)


SyncAction = NewType("SyncAction", dict)
