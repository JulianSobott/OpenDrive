"""
:module: OpenDrive.general.synchronization
:synopsis: 
:author: Julian Sobott

public classes
---------------

.. autoclass:: XXX
    :members:


public functions
----------------

.. autofunction:: XXX

private functions
-----------------


"""
import os
import shutil


def delete_file(abs_file_path: str, implicit=True):
    """For now just deletes the file. A backup system could be added later."""
    try:
        os.remove(abs_file_path)
    except FileNotFoundError as e:
        if not implicit:
            raise e


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
