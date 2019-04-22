import os
import shutil
from typing import Tuple
import uuid

import server_side
from OpenDrive.server_side import database
from OpenDrive.server_side import authentication
from OpenDrive.server_side import paths as server_paths
from general.database import delete_db_file

from tests.server_side.database import h_setup_server_database


def h_deactivate_set_user_authenticated(func):
    """Deactivates the function, that is only available when a client is connected"""
    def wrapper(*args):
        copy_set_user_authenticated = authentication._set_user_authenticated
        authentication._set_user_authenticated = lambda user_id: None
        ret = func(*args)
        authentication._set_user_authenticated = copy_set_user_authenticated
        return ret
    return wrapper


@h_deactivate_set_user_authenticated
def h_register_dummy_user_device() -> Tuple[database.User, database.Device, database.Token]:
    h_setup_server_database()

    username = "Anne"
    password = "2hj:_sAdf"
    email = None
    mac = str(uuid.getnode())
    token = authentication.register_user_device(username, password, mac, email)
    user = database.User(1, username, password, email)
    device = database.Device.get_by_mac(mac)

    return user, device, token


def h_clear_init_server_folders():
    """
    server: OpenDrive/local/server_side/ROOT/
    """
    shutil.rmtree(server_paths.FOLDERS_ROOT, ignore_errors=True)
    os.makedirs(server_paths.FOLDERS_ROOT, exist_ok=True)


def h_delete_recreate_server_db():
    delete_db_file(server_side.paths.SERVER_DB_PATH)
    server_side.database.create_database()