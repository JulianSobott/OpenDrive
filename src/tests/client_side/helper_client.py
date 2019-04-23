import uuid

from OpenDrive import client_side
from OpenDrive.server_side import database
from OpenDrive.client_side import authentication
from OpenDrive.general.database import delete_db_file


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
