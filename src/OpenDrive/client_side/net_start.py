from OpenDrive import net_interface


def connect():
    address = ("127.0.0.1", 5000)
    net_interface.ServerCommunicator.connect(address)
    test()


def test():
    net_interface.server.test()


def close_connection():
    net_interface.ServerCommunicator.close_connection()


if __name__ == '__main__':
    connect()

