from OpenDrive import net_interface


def connect(blocking=True, timeout=float("inf")):
    address = ("127.0.0.1", 5000)
    return net_interface.ServerCommunicator.connect(address, blocking=blocking, timeout=timeout)


def close_connection():
    net_interface.ServerCommunicator.close_connection()


if __name__ == '__main__':
    connect()

