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
import os

from OpenDrive.general.od_logging import setup_logger
from OpenDrive.general import paths as gen_paths

pynetworking.Logging.logger.setLevel(logging.WARNING)

log_to_file = False
if log_to_file:
    os.makedirs(gen_paths.SERVER_LOGS, exist_ok=True)
    log_file = gen_paths.normalize_path(gen_paths.SERVER_LOGS, "all.log")
else:
    log_file = None


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


logger_general = setup_logger("General", log_file)
logger_network = setup_logger("Network", log_file)
