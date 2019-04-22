from OpenDrive import client_side
from OpenDrive.general.database import delete_db_file

from tests.helper_all import h_clear_init_all_folders
from tests.server_side.database import h_setup_server_database
from tests.server_side.helper_server import h_register_dummy_user_device


def h_delete_recreate_client_db():
    delete_db_file(client_side.paths.LOCAL_DB_PATH)
    client_side.database.create_database()


def h_register_dummy_user_device_client():
    user, device, token = h_register_dummy_user_device()
    client_side.authentication._save_received_token(token)
    return user, device, token
