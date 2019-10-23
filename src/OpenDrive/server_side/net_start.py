import pynetworking as net

import sys
import os
import multiprocessing

sys.path.insert(0, os.path.abspath('../../'))

from OpenDrive import net_interface
from OpenDrive.server_side.od_logging import logger
from OpenDrive.server_side.database import general as db


def start(queue: multiprocessing.Queue = multiprocessing.Queue()):
    try:
        db.create_database()
    except FileExistsError:
        pass
    address = ("0.0.0.0", 5000)
    client_manager = net.ClientManager(address, net_interface.ClientCommunicator)
    client_manager.start()
    logger.debug(f"Server is now listening on {address}")
    try:
        while True:
            msg = queue.get()
            if msg == "Stop":
                break
    finally:
        client_manager.stop_listening()
        client_manager.stop_connections()
        logger.debug("Closed Server")


if __name__ == '__main__':
    net.Logging.logger.setLevel(10)
    start(multiprocessing.Queue())
