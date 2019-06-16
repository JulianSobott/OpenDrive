import datetime
import uuid

from OpenDrive.general.database import delete_db_file
from OpenDrive.server_side import database, paths
from OpenDrive.server_side.database import Token


def h_setup_server_database() -> None:
    """clear and create the server database file."""
    delete_db_file(paths.SERVER_DB_PATH)
    database.create_database()


def h_create_dummy_user() -> database.User:
    username = "Tom"
    password = "asj&kdkl$asjd345a!d:-"
    email = "Tom@gmail.com"
    user_id = database.User.create(username, password, email)
    return database.User(user_id, username, password, email)


def h_create_dummy_device() -> database.Device:
    user_id = 1
    mac_address = str(uuid.getnode())
    token = Token(32)
    token_expires = datetime.datetime(2020, 12, 31)
    device_id = database.Device.create(user_id, mac_address, token, token_expires)
    return database.Device(user_id, device_id, mac_address, token, token_expires)
