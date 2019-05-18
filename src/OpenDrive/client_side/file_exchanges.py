"""
:module: OpenDrive.client_side.file_exchanges
:synopsis: Exchange files over the network
:author: Julian Sobott
    
public functions
-----------------

.. autofunction:: get_file

"""
import pynetworking as net
import os

from OpenDrive.general import file_exchanges as gen_file_exchanges
from OpenDrive import net_interface


def get_file(abs_src_path: str, abs_dest_path: str) -> net.File:
    """Call to send a file from the client to the server."""
    return gen_file_exchanges.get_file(abs_src_path, abs_dest_path)


def get_dir(abs_src_path: str, abs_dest_path: str) -> None:
    return gen_file_exchanges.get_dir(abs_src_path, abs_dest_path, net_interface.server.pull_file,
                                      net_interface.server.make_dirs)


def pull_file(rel_server_path: str, abs_client_path: str) -> None:
    """Pulls a file from the server and saves it at the client"""
    os.makedirs(os.path.split(abs_client_path)[0], exist_ok=True)
    file = net_interface.server.get_file(rel_server_path, abs_client_path)
