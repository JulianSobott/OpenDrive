"""
:module: OpenDrive.server_side.folders
:synopsis: Manages all folders, that are located at the server
:author: Julian Sobott

public classes
---------------

    
public functions
-----------------

.. autofunction:: add_folder

private classes
----------------

.. autofunction:: _create_physical_folder

private functions
------------------

"""
import os
import shutil
from pathlib import Path

from OpenDrive.server_side import database
from OpenDrive.server_side import paths
from OpenDrive.server_side.od_logging import logger
from OpenDrive.server_side.database import User


def add_folder(user: User, folder_name: str):
    """Creates a new folder at the users path and creates a new entry at the DB."""
    _create_physical_folder(user, folder_name)
    database.Folder.create(user.user_id, folder_name)


def _create_physical_folder(user: User, folder_name: str):
    """Creates a new folder at the harddrive."""
    users_root = _get_users_root_folder(user)
    new_folder_path = users_root.joinpath(folder_name)
    new_folder_path.mkdir()


def create_folder_for_new_user(user: User) -> None:
    users_root = _get_users_root_folder(user)
    assert not os.path.exists(str(users_root)), "User folder already exists!"
    os.makedirs(str(users_root))


def _get_users_root_folder(user: User) -> Path:
    user_path = f"user_{user.user_id}"
    return Path(paths.FOLDERS_ROOT, user_path)

