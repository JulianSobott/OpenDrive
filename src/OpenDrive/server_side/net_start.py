import pynetworking as net
import time

from OpenDrive import net_interface
from OpenDrive.server_side.od_logging import logger
import multiprocessing


def start(queue: multiprocessing.Queue):
    address = ("0.0.0.0", 5000)
    client_manager = net.ClientManager(address, net_interface.ClientCommunicator)
    client_manager.start()
    try:
        while True:
            msg = queue.get()
            if msg:
                break
    finally:
        client_manager.stop_listening()
        client_manager.stop_connections()
        logger.debug("Closed Server")


if __name__ == '__main__':
    start(multiprocessing.Queue())
