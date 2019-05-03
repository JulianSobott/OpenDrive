"""
:module: OpenDrive.server_side.synchronization
:synopsis: Server side synchronization
:author: Julian Sobott

public functions
----------------

.. autofunction:: get_changes

private functions
-----------------


"""
import pynetworking as net
import os

from OpenDrive import net_interface
from OpenDrive.server_side import paths as server_paths


def get_changes(dest_path: str) -> net.File:
    user: net_interface.ClientCommunicator = net.ClientManager().get()

    device_id = ""  # TODO
    user_path = server_paths.get_users_root_folder(user.user_id)
    changes_path = os.path.join(user_path, f"changes_{device_id}.json")
    return net.File(changes_path, dest_path)
