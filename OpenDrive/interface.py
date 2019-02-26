import networking as net


class ServerFunctions(net.ServerFunctions):
    pass


class ClientFunctions(net.ClientFunctions):
    pass


class ServerCommunicator(net.ServerCommunicator):
    remote_functions = ServerFunctions
    local_functions = ClientFunctions


class ClientCommunicator(net.ClientCommunicator):
    remote_functions = ClientFunctions
    local_functions = ServerFunctions
