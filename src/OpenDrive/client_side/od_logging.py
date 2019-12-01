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
from OpenDrive.general.od_logging import setup_logger

pynetworking.Logging.logger.setLevel(logging.WARNING)


logger_gui = setup_logger("GUI")
logger_general = setup_logger("General")
logger_network = setup_logger("Network")
logger_sync = setup_logger("Sync")
logger_security = setup_logger("Security")
