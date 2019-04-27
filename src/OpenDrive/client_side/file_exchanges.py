"""
:module: OpenDrive.client_side.file_exchanges
:synopsis: Send and receive files over the network
:author: Julian Sobott

public classes
---------------

.. autoclass:: XXX
    :members:
    
public functions
-----------------

.. autofunction:: get_file

private classes
----------------

private functions
------------------

"""
import pynetworking as net

from OpenDrive.general import file_exchanges as gen_file_exchanges
from OpenDrive import net_interface
from OpenDrive.general.file_exchanges import Action


def get_file(abs_src_path: str, abs_dest_path: str) -> net.File:
    return gen_file_exchanges.get_file(abs_src_path, abs_dest_path)
