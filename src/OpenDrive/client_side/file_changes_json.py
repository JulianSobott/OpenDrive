"""
:module: OpenDrive.client_side.file_changes_json
:synopsis: Read and edit the json file, that stores folders and changes
:author: Julian Sobott

public functions
-----------------

.. autofunction:: init_file

private classes
----------------

private functions
------------------

"""
import json
import os

from OpenDrive.client_side import paths as client_paths

__all__ = ["init_file"]


def init_file():
    os.makedirs(client_paths.LOCAL_CLIENT_DATA, exist_ok=True)
    with open(client_paths.LOCAL_JSON_PATH, "w+") as file:
        all_folders = []
        json.dump(all_folders, file)
