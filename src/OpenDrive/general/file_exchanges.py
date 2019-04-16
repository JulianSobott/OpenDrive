"""
:module: OpenDrive.general.file_exchanges
:synopsis: Send and receive files over the network
:author: Julian Sobott
public functions
-----------------
.. autofunction:: get_file

private functions
------------------
"""
import os
import pynetworking as net


def get_file(abs_file_src_path: str, abs_file_dest_path: str) -> net.File:
    if os.path.isfile(abs_file_src_path):
        return net.File(abs_file_src_path, abs_file_dest_path)
    else:
        raise FileNotFoundError
