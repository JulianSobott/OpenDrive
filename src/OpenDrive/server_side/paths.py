"""
:module: OpenDrive.server_side.paths
:synopsis: All important paths at the server-side
:author: Julian Sobott

public constants
-----------------

"""
import pynetworking as net

from OpenDrive.general.paths import *
from OpenDrive import net_interface


LOCAL_SERVER_DATA = os.path.join(LOCAL_DATA, "server_side/")

SERVER_DB_PATH = os.path.join(LOCAL_SERVER_DATA, "server_data.db")

FOLDERS_ROOT = os.path.join(LOCAL_SERVER_DATA, "ROOT/")


def rel_user_path_to_abs(rel_path: str, user_id: int = -1):
    if user_id == -1:
        client: net_interface.ClientCommunicator = net.ClientManager().get()
        user_id = client.user_id
    return os.path.join(get_users_root_folder(user_id), rel_path)


def get_users_root_folder(user_id: int) -> str:
    return os.path.join(FOLDERS_ROOT, f"user_{user_id}/")