from typing import Tuple
import uuid

from OpenDrive.server_side import database
from OpenDrive.server_side import authentication

from tests.server_side.database import h_setup_server_database


def h_deactivate_set_user_authenticated(func):
    """Deactivates the function, that is only available when a client is connected"""
    def wrapper(*args):
        copy_set_user_authenticated = authentication._set_user_authenticated
        authentication._set_user_authenticated = lambda user_id: None
        func(*args)
        authentication._set_user_authenticated = copy_set_user_authenticated
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
