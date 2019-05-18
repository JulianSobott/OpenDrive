"""
:module: OpenDrive.client_side.file_exchanges
:synopsis: Exchange files over the network
:author: Julian Sobott
    
public functions
-----------------

.. autofunction:: get_file

"""
import pynetworking as net

from OpenDrive.general import file_exchanges as gen_file_exchanges


def get_file(abs_src_path: str, abs_dest_path: str) -> net.File:
    """Call to send a file from the client to the server."""
    return gen_file_exchanges.get_file(abs_src_path, abs_dest_path)
