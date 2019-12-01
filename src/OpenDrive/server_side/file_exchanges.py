"""
:module: OpenDrive.server_side.file_exchanges
:synopsis: Send and receive files over the network
:author: Julian Sobott

public functions
-----------------

.. autofunction:: get_file
.. autofunction:: make_dirs
.. autofunction:: move
.. autofunction:: remove_file

"""
import os
import pynetworking as net

from OpenDrive.general import file_exchanges as gen_file_exchanges
from OpenDrive import net_interface
from OpenDrive.server_side import paths as server_paths
from OpenDrive.server_side.authentication import requires_authentication
from OpenDrive.server_side.od_logging import client_logger_sync


@requires_authentication
def get_file(rel_src_path: str, abs_file_dest_path: str) -> net.File:
    client_logger_sync().info(f"Get file: rel_src_path={rel_src_path}, abs_file_dest_path={abs_file_dest_path}")
    abs_file_src_path = server_paths.rel_user_path_to_abs(rel_src_path)
    return gen_file_exchanges.get_file(abs_file_src_path, abs_file_dest_path)


@requires_authentication
def get_dir(rel_src_path: str, abs_dest_path: str) -> None:
    client_logger_sync().info(f"Get dir: rel_src_path={rel_src_path}, abs_dest_path={abs_dest_path}")
    abs_src_path = server_paths.rel_user_path_to_abs(rel_src_path)
    return gen_file_exchanges.get_dir(abs_src_path, abs_dest_path,
                                      net_interface.get_user().remote_functions.pull_file,
                                      net_interface.get_user().remote_functions.make_dirs)


def move(rel_src_path: str, rel_dest_path: str) -> None:
    """paths are relative to users root folder (ROOT/user_X/).
    Folders that don't exist are created"""
    client_logger_sync().info(f"Move file: rel_src_path={rel_src_path}, rel_dest_path={rel_dest_path}")
    abs_src_path = server_paths.rel_user_path_to_abs(rel_src_path)
    abs_dest_path = server_paths.rel_user_path_to_abs(rel_dest_path)
    return gen_file_exchanges.move(abs_src_path, abs_dest_path)


@requires_authentication
def make_dirs(rel_path: str, exist_ok: bool = True):
    client_logger_sync().info(f"Make dirs: rel_path={rel_path}, exist_ok={exist_ok}")
    abs_path = server_paths.rel_user_path_to_abs(rel_path)
    return gen_file_exchanges.make_dirs(abs_path, exist_ok)


def remove_file_dir(rel_path: str, only_empty: bool = False):
    client_logger_sync().info(f"Remove file/dir: rel_path={rel_path}, only_empty={only_empty}")
    abs_path = server_paths.rel_user_path_to_abs(rel_path)
    if os.path.isdir(abs_path):
        gen_file_exchanges.remove_dir(abs_path, only_empty)
    else:
        gen_file_exchanges.remove_file(abs_path)


@requires_authentication
def pull_file(abs_client_path: str, rel_server_path: str) -> None:
    """Pulls a file from the client and saves it at the server. The server path is relative to the users root folder.
    Folders that don't exist are created."""
    client_logger_sync().info(f"Pull file: abs_client_path={abs_client_path}, rel_server_path={rel_server_path}")
    client = net_interface.get_user()
    abs_server_path = server_paths.rel_user_path_to_abs(rel_server_path, client.user_id)
    os.makedirs(os.path.split(abs_server_path)[0], exist_ok=True)
    file = client.remote_functions.get_file(abs_client_path, abs_server_path)


def pull_dir(abs_client_path: str, rel_server_path: str) -> None:
    """Pulls a folder with all it files and subfolders from the client."""
    client_logger_sync().info(f"Pull dir: abs_client_path={abs_client_path}, rel_server_path={rel_server_path}")
    client = net_interface.get_user()
    abs_server_path = server_paths.rel_user_path_to_abs(rel_server_path, client.user_id)
    os.makedirs(abs_server_path, exist_ok=True)
    client.remote_functions.get_dir(abs_client_path, abs_server_path)
