"""
@author: Julian Sobott
@created: 13.11.2018

Available loggers:

- **logger_general:** Logging the program flow
- **logger_network:** Logging network stuff

Available loggers per client:

- **logger_sync:** Logging synchronization stuff
- **logger_security:** Logging security relevant stuff like authentication
- **logger_network:** Logging network stuff
"""
import logging
import pynetworking

from OpenDrive.general.od_logging import setup_logger

pynetworking.Logging.logger.setLevel(logging.WARNING)


def client_logger_sync():
    from OpenDrive.net_interface import get_client_id
    client_name = get_client_id()
    return setup_logger(f"[{client_name}] Sync")


def client_logger_security():
    from OpenDrive.net_interface import get_client_id
    client_name = get_client_id()
    return setup_logger(f"[{client_name}] Security")


def client_logger_network():
    from OpenDrive.net_interface import get_client_id
    client_name = get_client_id()
    return setup_logger(f"[{client_name}] Network")


logger_general = setup_logger("General")
logger_network = setup_logger("Network")

