import pynetworking as net


class ServerFunctions(net.ServerFunctions):
    """All server functions, that can be called by the client"""
    from OpenDrive.server_side.authentication import register_user_device, login_manual_user_device, login_auto


class ClientFunctions(net.ClientFunctions):
    """All client functions, that can be called by the server"""
    pass


class ServerCommunicator(net.ServerCommunicator):
    remote_functions = ServerFunctions
    local_functions = ClientFunctions


class ClientCommunicator(net.ClientCommunicator):
    remote_functions = ClientFunctions
    local_functions = ServerFunctions

    def __init__(self, id_, address, connection, on_close):
        super().__init__(id_, address, connection, on_close)
        self._is_authenticated = False

    @property
    def is_authenticated(self) -> bool:
        return self._is_authenticated

    @is_authenticated.setter
    def is_authenticated(self, val: bool) -> None:
        self._is_authenticated = val


server = ServerCommunicator.remote_functions
