"""
:module: OpenDrive.server_side.folders
:synopsis: Manages all folders, that are located at the server
:author: Julian Sobott

public functions
-----------------

.. autofunction:: add_folder

.. autofunction:: create_folder_for_new_user

.. autofunction:: get_users_root_folder

private functions
------------------

.. autofunction:: _create_physical_folder

"""
import os
from pathlib import Path
import pynetworking as net

from OpenDrive.server_side import database
from OpenDrive.server_side import paths
from OpenDrive.server_side.database import User
from OpenDrive import net_interface


def add_folder(folder_name: str):
    """Creates a new folder at the users path and creates a new entry at the DB."""
    user: net_interface.ClientCommunicator = net.ClientManager().get()
    _add_folder_to_user(user.user_id, folder_name)


def _add_folder_to_user(user_id: int, folder_name: str):
    """Creates a new folder at the users path and creates a new entry at the DB."""
    _create_physical_folder(user_id, folder_name)
    database.Folder.create(user_id, folder_name)


def _create_physical_folder(user_id: int, folder_name: str):
    """Creates a new folder at the harddrive."""
    users_root = get_users_root_folder(user_id)
    new_folder_path = users_root.joinpath(folder_name)
    new_folder_path.mkdir()


def create_folder_for_new_user(user: User) -> None:
    """For every user a folder in the root folder is created. Inside this new  folder every synchronized folder is
    stored"""
    users_root = get_users_root_folder(user.user_id)
    assert not os.path.exists(str(users_root)), "User folder already exists!"
    os.makedirs(str(users_root))


def get_users_root_folder(user_id: int) -> Path:
    user_path = f"user_{user_id}"
    return Path(paths.FOLDERS_ROOT, user_path)
