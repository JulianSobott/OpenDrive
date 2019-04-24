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


class PullAction(Action):
    """Action, when the server needs to pull a file from the client."""

    def __init__(self, abs_local_path: str, abs_remote_path: str):
        super().__init__(abs_local_path)
        self.abs_remote_path = abs_remote_path

    def run(self):
        client: net_interface.ClientCommunicator = net.ClientManager().get()
        client.remote_functions.get_file(self.abs_remote_path, self.abs_local_path)
