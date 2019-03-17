from OpenDrive import net_interface
import networking as net
import time


def start():
    address = ("127.0.0.1", 5000)
    client_manager = net.ClientManager(address, net_interface.ClientCommunicator)
    client_manager.start()
    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            break
    client_manager.stop_listening()
    client_manager.stop_connections()


if __name__ == '__main__':
    start()
