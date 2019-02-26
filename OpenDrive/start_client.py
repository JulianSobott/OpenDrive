if __name__ == '__main__':
    import interface
    from Logging import logger
else:
    from OpenDrive import interface
    from OpenDrive.Logging import logger


def start_client(address: tuple):
    interface.ServerCommunicator.connect(address, blocking=True)
    logger.debug(id(interface.ServerCommunicator))


def stop_client():
    interface.ServerCommunicator.close_connection()


if __name__ == '__main__':
    start_client(("127.0.0.1", 5000))