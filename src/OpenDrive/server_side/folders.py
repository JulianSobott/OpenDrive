"""
:module: OpenDrive.server_side.folders
:synopsis: Manages all folders, that are located at the server
:author: Julian Sobott

public functions
-----------------

.. autofunction:: add_folder
.. autofunction:: create_folder_for_new_user
.. autofunction:: get_users_root_folder
.. autofunction:: get_all_available_folders
.. autofunction:: generate_content_of_folder

private functions
------------------

.. autofunction:: _add_folder_to_user
.. autofunction:: _create_physical_folder

"""
import os
from pathlib import Path
from typing import List

from OpenDrive.server_side import database
from OpenDrive.server_side import paths
from OpenDrive.server_side import path_utils
from OpenDrive.server_side.database import User
from OpenDrive.server_side import file_changes_json
from OpenDrive.general import merge_folders as gen_merge_folders
from OpenDrive import net_interface
from OpenDrive.server_side.decorators import requires_authentication


@requires_authentication
def add_folder(folder_name: str) -> bool:   # TODO: DO we allow paths or only names? folder/path vs path
    """If the folder does not exist, creates a new folder at the users path and creates a new entry at the DB.
    Returns True if a new folder is created and added. If the folder already exists return False."""
    user = net_interface.get_user()
    if database.Folder.get_by_user_and_name(user.user_id, folder_name) is None:
        _add_folder_to_user(user.user_id, folder_name)
        return True
    else:
        return False


def create_folder_for_new_user(user: User) -> None:
    """For every user a folder in the root folder is created. Inside this new  folder every synchronized folder is
    stored"""
    users_root = path_utils.get_users_root_folder(user.user_id)
    assert not os.path.exists(users_root), "User folder already exists!"
    os.makedirs(str(users_root))


def get_users_root_folder(user_id: int) -> Path:
    user_path = f"user_{user_id}"
    return Path(paths.FOLDERS_ROOT, user_path)


@requires_authentication
def generate_content_of_folder(folder_name: str, only_files_list=False, user_id: int = -1):
    if user_id == -1:
        user_id = net_interface.get_user_id()
    abs_path = path_utils.rel_user_path_to_abs(folder_name, user_id)
    return gen_merge_folders.generate_content_of_folder(abs_path, only_files_list, folder_name)


@requires_authentication
def get_all_available_folders(user_id: int = -1) -> List[str]:
    if user_id == -1:
        user_id = net_interface.get_user_id()
    folders = database.Folder.get_by_user(user_id)
    return [folder.folder_name for folder in folders]


def _add_folder_to_user(user_id: int, folder_name: str):
    """Creates a new folder at the users path and creates a new entry at the DB and json_file."""
    _create_physical_folder(user_id, folder_name)
    database.Folder.create(user_id, folder_name)
    file_changes_json.add_folder(folder_name)


def _create_physical_folder(user_id: int, folder_name: str):
    """Creates a new folder at the harddrive."""
    users_root = path_utils.get_users_root_folder(user_id)
    new_folder_path = paths.normalize_path(users_root, folder_name)
    os.mkdir(new_folder_path)
