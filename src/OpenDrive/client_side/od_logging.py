"""
@author: Julian Sobott
@created: 13.11.2018

Available loggers:

- **logger_general:** Logging the program flow
- **logger_network:** Logging network stuff
- **logger_sync:** Logging synchronization stuff
- **logger_gui:** Logging gui stuff
- **logger_security:** Logging security relevant stuff like authentication
"""
import logging
import pynetworking
import os

from OpenDrive.general.od_logging import setup_logger
from OpenDrive.general import paths as gen_paths

pynetworking.Logging.logger.setLevel(logging.WARNING)

log_to_file = False
if log_to_file:
    os.makedirs(gen_paths.CLIENT_LOGS, exist_ok=True)
    log_file = gen_paths.normalize_path(gen_paths.CLIENT_LOGS, "all.log")
else:
    log_file = None

logger_gui = setup_logger("GUI", log_file)
logger_general = setup_logger("General", log_file)
logger_network = setup_logger("Network", log_file)
logger_sync = setup_logger("Sync", log_file)
logger_security = setup_logger("Security", log_file)
