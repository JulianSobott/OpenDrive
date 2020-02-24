"""
:module: OpenDrive.client_side.net_start
:synopsis: Establish a connection to the server
:author: Julian Sobott


public functions
----------------

.. autofunction:: connect
.. autofunction:: close_connection

"""
from pynetworking import client
from OpenDrive import net_interface
from OpenDrive.client_side.od_logging import logger_network


def connect(blocking=True, timeout=float("inf")):
    """Connects to the server. Default is try infinity long till the connection is successful."""
    address = "192.168.178.26", 5000
    address = "127.0.0.1", 5000
    logger_network.info(f"Connecting to server: address={address}, blocking={blocking}, timeout={timeout}")
    ret = net_interface.ServerCommunicator.connect(address, blocking=blocking, timeout=timeout)
    logger_network.info(f"{'Successfully connected to server' if ret else 'Failed to connect to server'}")
    return ret


def close_connection():
    logger_network.info("Start close server connection")
    net_interface.ServerCommunicator.close_connection()
    logger_network.info("Finished close server connection")


if __name__ == '__main__':
    connect()
