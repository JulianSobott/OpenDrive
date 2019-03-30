import networking as net

net.Logging.logger.setLevel(10)


class ServerCommunicator:
    remote_functions = None


class ClientCommunicator:
    remote_functions = None


class ServerFunctions(net.ServerFunctions):
    """All server functions, that can be called by the client"""
    from OpenDrive.server_side.net_start import test
    from OpenDrive.server_side.authentication import register_user_device


class ClientFunctions(net.ClientFunctions):
    """All client functions, that can be called by the server"""
    pass


class ServerCommunicator(net.ServerCommunicator):
    remote_functions = ServerFunctions
    local_functions = ClientFunctions


class ClientCommunicator(net.ClientCommunicator):
    remote_functions = ClientFunctions
    local_functions = ServerFunctions
