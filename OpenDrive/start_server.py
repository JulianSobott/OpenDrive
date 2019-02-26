import networking as net

if __name__ == '__main__':
    import interface
    from Logging import logger
else:
    from OpenDrive import interface
    from OpenDrive.Logging import logger

client_manager: net.ClientManager


def start_server(address: tuple):
    global client_manager
    client_manager = net.ClientManager(address, interface.ClientCommunicator)
    client_manager.start()


def stop_server():
    global client_manager
    client_manager.stop_listening()
    client_manager.stop_connections()


if __name__ == '__main__':
    start_server(("", 5000))
    print("finish")
