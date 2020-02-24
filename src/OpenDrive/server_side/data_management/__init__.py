"""
:module: OpenDrive.
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
from typing import Union, List

from OpenDrive.server_side.data_management.data_classes import User, File, Folder
from OpenDrive.server_side.data_management.status import Status, ErrorCode
from OpenDrive.server_side import paths as server_paths

ERR_FILE_NOT_EXISTS = ErrorCode((1000, "ERR_FILE_NOT_EXISTS"))
ERR_NOT_A_FOLDER = ErrorCode((1001, "ERR_NOT_A_FOLDER"))


def get_files_by_user(user: User, rel_path: str, depth: int = 0, max_files: int = 999) \
        -> Status[List[Union[File, Folder]]]:
    """Get a list of files from a user.

    The query starts at rel_path.
    The bigger the depth the less often this function needs to be called, when the filesystem is traversed, but
    the data can become very huge. Default depth is 0, meaning that no sub-folders are opened.

    :param user: The user for which the files are requested
    :param rel_path: The path where the query should start. Root folder is /
    :param depth: How deep the sub-folders are queried.
    :param max_files:
    :return: A list of files and folders
    """
    def _get_files(_abs_root: str, _rel_path: str, remaining_depth: int) -> List[Union[File, Folder]]:
        files = []
        _abs_path = server_paths.normalize_path(_abs_root, _rel_path)
        with os.scandir(_abs_path) as it:
            for f in it:
                file = File("No_UID_yet", f.name, _rel_path, "No_parent_UID_yet", user, [], {})
                if f.is_file():
                    files.append(file)
                if f.is_dir():
                    if remaining_depth > 0:
                        rel = server_paths.normalize_path(_rel_path, f.name)
                        folder = Folder(file, _get_files(_abs_root, rel, remaining_depth - 1))
                    else:
                        folder = Folder(file, [], files_not_listed=True)
                    files.append(folder)
        return files
    rel_path = "." if rel_path == "/" else rel_path      # needed when joining
    abs_root = server_paths.get_users_root_folder(user)
    abs_path = server_paths.normalize_path(abs_root, rel_path)
    if not os.path.exists(abs_path):
        return Status.fail(ERR_FILE_NOT_EXISTS)
    if not os.path.isdir(abs_path):
        return Status.fail(ERR_NOT_A_FOLDER)
    final_files = _get_files(abs_root, rel_path, remaining_depth=depth)
    return Status.success(final_files)
