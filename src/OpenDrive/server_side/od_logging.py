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

from OpenDrive.general.od_logging import setup_logger, log_system
from OpenDrive.general import paths as gen_paths

pynetworking.Logging.logger.setLevel(logging.WARNING)

logger_general: logging.Logger = logging.getLogger("General")
logger_network: logging.Logger = logging.getLogger("Network")

client_loggers = {}
log_to_file = True


def get_client_file_path(client_name):
    if log_to_file:
        return gen_paths.normalize_path(gen_paths.SERVER_LOGS, f"client_{client_name}.log")
    else:
        return None


def _client_logger(name):
    from OpenDrive.net_interface import get_client_id
    client_name = get_client_id()
    logger_name = f"[{client_name}] {name}"
    if logger_name in client_loggers:
        return client_loggers[logger_name]
    else:
        client_loggers[logger_name] = setup_logger(logger_name, get_client_file_path(client_name))
        return client_loggers[logger_name]


def client_logger_sync():
    return _client_logger("Sync")


def client_logger_security():
    return _client_logger("Security")


def client_logger_network():
    return _client_logger("Network")


def init_logging():
    global logger_network, logger_general
    if log_to_file:
        os.makedirs(gen_paths.SERVER_LOGS, exist_ok=True)
        log_file = gen_paths.normalize_path(gen_paths.SERVER_LOGS, "all.log")
    else:
        log_file = None
    logger_general = setup_logger("General", log_file)
    logger_network = setup_logger("Network", log_file)
    log_system(log_file)
