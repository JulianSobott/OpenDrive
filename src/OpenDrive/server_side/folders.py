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

from OpenDrive.server_side import database
from OpenDrive.server_side import paths
from OpenDrive.server_side.od_logging import logger


def add_folder(user_id: int, folder_name: str):
    """Creates a new folder at the users path and creates a new entry at the DB."""
    _create_physical_folder(user_id, folder_name)
    database.Folder.create(user_id, folder_name)


def _create_physical_folder(user_id: int, folder_name: str):
    """Creates a new folder at the harddrive."""
    user_path = f"user_{user_id}"
    folder_path = os.path.join(paths.FOLDERS_ROOT, user_path, folder_name)
    try:
        os.mkdir(folder_path)
    except FileNotFoundError:
        logger.error("Cannot create folder, because the parent folder does not exist!")
