"""
:module: OpenDrive.server_side.file_exchanges
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

from OpenDrive.server_side import folders
from OpenDrive.server_side.database import User
from OpenDrive.general import file_exchanges as gen_file_exchanges
from OpenDrive import net_interface
from OpenDrive.general.file_exchanges import Action


def get_file(rel_src_path: str, abs_file_dest_path: str) -> net.File:
    client: net_interface.ClientCommunicator = net.ClientManager().get()
    user: User = User.from_id(client.user_id)
    abs_file_src_path = os.path.join(str(folders.get_users_root_folder(user)), rel_src_path)
    return gen_file_exchanges.get_file(abs_file_src_path, abs_file_dest_path)


class PullAction(Action):
    """Action, when the server needs to pull a file from the client."""

    def __init__(self, abs_local_path: str, abs_remote_path: str):
        super().__init__(abs_local_path)
        self.abs_remote_path = abs_remote_path

    def run(self):
        client: net_interface.ClientCommunicator = net.ClientManager().get()
        client.remote_functions.get_file(self.abs_remote_path, self.abs_local_path)
