import os
import uuid

from OpenDrive import client_side
from OpenDrive.server_side import database
from OpenDrive.client_side import authentication
from OpenDrive.general.database import delete_db_file
from client_side import paths as client_paths

from tests.server_side.database import h_setup_server_database


def h_delete_recreate_client_db():
    delete_db_file(client_side.paths.LOCAL_DB_PATH)
    client_side.database.create_database()


def h_register_dummy_user_device_client() -> database.User:
    h_setup_server_database()

    username = "Anne"
    password = "2hj:_sAdf"
    email = None
    user = database.User(1, username, password, email)
    status = authentication.register_user_device(username, password, email)

    return user


def h_create_client_dummy_file():
    """OpenDrive/local/client_side/DUMMY/dummy.txt"""
    file_name = "dummy.txt"
    rel_path = os.path.join("DUMMY", file_name)
    path = os.path.join(client_paths.LOCAL_CLIENT_DATA, rel_path)
    os.makedirs(os.path.split(path)[0], exist_ok=True)
    with open(path, "w+") as file:
        file.write("Hello" * 10)
    return path


def h_get_dummy_folder_data():
    path = client_paths.normalize_path(client_paths.LOCAL_CLIENT_DATA)
    include = [".*"]
    exclude = []
    return path, include, exclude
