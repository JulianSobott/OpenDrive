import pynetworking as net


class ServerFunctions(net.ServerFunctions):
    """All server functions, that can be called by the client"""
    from OpenDrive.server_side.authentication import register_user_device, login_manual_user_device, login_auto, \
        logout
    from OpenDrive.server_side.file_exchanges import get_file, pull_file, make_dirs, get_dir
    from OpenDrive.server_side.synchronization import get_changes, execute_actions
    from OpenDrive.server_side.folders import add_folder, generate_content_of_folder


class ClientFunctions(net.ClientFunctions):
    """All client functions, that can be called by the server"""
    from OpenDrive.general.file_exchanges import get_file, make_dirs
    from OpenDrive.client_side.file_exchanges import get_dir, pull_file
    from OpenDrive.client_side.synchronization import trigger_server_synchronization


class ServerCommunicator(net.ServerCommunicator):
    remote_functions = ServerFunctions
    local_functions = ClientFunctions


class ClientCommunicator(net.ClientCommunicator):
    remote_functions = ClientFunctions
    local_functions = ServerFunctions

    def __init__(self, id_, address, connection, on_close):
        super().__init__(id_, address, connection, on_close)
        self._is_authenticated = False
        self.user_id = -1
        self.device_id = -1

    @property
    def is_authenticated(self) -> bool:
        return self._is_authenticated

    @is_authenticated.setter
    def is_authenticated(self, val: bool) -> None:
        self._is_authenticated = val


server = ServerCommunicator.remote_functions


def get_user_id() -> int:
    user: ClientCommunicator = net.ClientManager().get()
    return user.user_id


def get_device_id() -> int:
    user: ClientCommunicator = net.ClientManager().get()
    return user.device_id


def get_user() -> ClientCommunicator:
    return net.ClientManager().get()
