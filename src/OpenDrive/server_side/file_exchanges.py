"""
:module: OpenDrive.server_side.file_exchanges
:synopsis: Send and receive files over the network
:author: Julian Sobott

public functions
-----------------

.. autofunction:: get_file
.. autofunction:: move_file
.. autofunction:: remove_file


private functions
------------------

"""
import os
import pynetworking as net

from OpenDrive.general import file_exchanges as gen_file_exchanges
from OpenDrive import net_interface
from OpenDrive.server_side import paths as server_paths


def get_file(rel_src_path: str, abs_file_dest_path: str) -> net.File:
    abs_file_src_path = server_paths.rel_user_path_to_abs(rel_src_path)
    return gen_file_exchanges.get_file(abs_file_src_path, abs_file_dest_path)


def move_file(rel_src_path: str, rel_dest_path: str) -> None:
    """paths are relative to users root folder (ROOT/user_X/).
    Folders that don't exist are created"""
    abs_src_path = server_paths.rel_user_path_to_abs(rel_src_path)
    abs_dest_path = server_paths.rel_user_path_to_abs(rel_dest_path)
    return gen_file_exchanges.move_file(abs_src_path, abs_dest_path)


def remove_file(rel_src_path: str) -> None:
    abs_src_path = server_paths.rel_user_path_to_abs(rel_src_path)
    return gen_file_exchanges.remove_file(abs_src_path)


def pull_file(abs_client_path: str, rel_server_path: str) -> None:
    """Pulls a file from the client and saves it at the server. The server path is relative to the users root folder.
    Folders that don't exist are created."""
    client: net_interface.ClientCommunicator = net.ClientManager().get()
    abs_server_path = server_paths.rel_user_path_to_abs(rel_server_path, client.user_id)
    os.makedirs(os.path.split(abs_server_path)[0], exist_ok=True)
    file = client.remote_functions.get_file(abs_client_path, abs_server_path)
