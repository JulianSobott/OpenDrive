"""
:module: OpenDrive.net_interface
:synopsis: Define all necessary stuff for the `pynetworking` library
:author: Julian Sobott

This program uses the `pynetworking <https://github.com/JulianSobott/pynetworking>`_ library for the communication
over the network. This library enables an easy way
of communication between multiple devices over a network. But to enable this some "complex" things must be setup first
in this module. To understand what exactly is done here have a look at the
`pynetworking documentation <https://pynetworking.readthedocs.io/en/latest/>`_.

public module members
----------------------

.. autodata:: server

public classes
-----------------

.. autoclass:: ServerCommunicator
.. autoclass:: ClientCommunicator

public functions
------------------

.. autofunction:: get_device_id
.. autofunction:: get_user
.. autofunction:: get_user_id

private classes
--------------------

.. autoclass:: ClientFunctions
    :show-inheritance:

.. autoclass:: ServerFunctions
    :show-inheritance:

"""
import pynetworking as net


net.Logging.logger.setLevel(30)


class ServerFunctions(net.ServerFunctions):
    """All server functions, that can be called by the client"""
    if net.global_data.IS_SERVER:
        from OpenDrive.server_side.authentication import register_user_device, login_manual_user_device, login_auto, \
            logout
        from OpenDrive.server_side.file_exchanges import get_file, pull_file, make_dirs, get_dir
        from OpenDrive.server_side.synchronization import get_changes, execute_actions
        from OpenDrive.server_side.folders import add_folder, generate_content_of_folder, get_all_available_folders
        from OpenDrive.server_side.file_changes_json import remove_handled_changes


class ClientFunctions(net.ClientFunctions):
    """All client functions, that can be called by the server"""
    if net.global_data.IS_CLIENT:
        from OpenDrive.general.file_exchanges import get_file, make_dirs

    @staticmethod
    def get_dir(abs_src_path: str, abs_dest_path: str) -> None:
        from OpenDrive.client_side.file_exchanges import get_dir
        return get_dir(abs_src_path, abs_dest_path)

    @staticmethod
    def pull_file(rel_server_path: str, abs_client_path: str) -> None:
        from OpenDrive.client_side.file_exchanges import pull_file
        return pull_file(rel_server_path, abs_client_path)

    @staticmethod
    def open_authentication_window():
        from OpenDrive.client_side.gui.main import open_authentication_window
        open_authentication_window()


class ServerCommunicator(net.ServerCommunicator):
    remote_functions = ServerFunctions
    local_functions = ClientFunctions


class ClientCommunicator(net.ClientCommunicator):
    remote_functions = ClientFunctions
    local_functions = ServerFunctions

    def __init__(self, id_, address, connection, on_close):
        super().__init__(id_, address, connection, on_close)
        # logger_network.info(f"New client connected: ID={id_}, address={address}")
        self._is_authenticated = False
        self.user_id = -1
        self.device_id = -1

    @property
    def is_authenticated(self) -> bool:
        return self._is_authenticated

    @is_authenticated.setter
    def is_authenticated(self, val: bool) -> None:
        self._is_authenticated = val

    def __repr__(self):
        return f"ClientCommunicator(id={self.id}, user_id={self.user_id}, device_id={self.device_id}, " \
               f"is_authenticated={self.is_authenticated})"


server = ServerCommunicator.remote_functions


def get_user_id() -> int:
    user: ClientCommunicator = net.ClientManager().get()
    return user.user_id


def get_device_id() -> int:
    user: ClientCommunicator = net.ClientManager().get()
    return user.device_id


def get_user() -> ClientCommunicator:
    return net.ClientManager().get()


def get_client_id() -> int:
    return net.ClientManager().get().id
