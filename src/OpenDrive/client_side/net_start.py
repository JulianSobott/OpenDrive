from OpenDrive import net_interface

server = net_interface.ServerCommunicator.remote_functions


def connect():
    address = ("127.0.0.1", 5000)
    net_interface.ServerCommunicator.connect(address, blocking=False)


def close_connection():
    net_interface.ServerCommunicator.close_connection()


if __name__ == '__main__':
    connect()

