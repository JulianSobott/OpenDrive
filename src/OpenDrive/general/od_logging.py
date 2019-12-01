"""
@author: Julian Sobott
@created: 13.11.2018
@brief:
@description:

@external_use:

@internal_use:

"""
import logging


def setup_logger(logger_name, log_file=None, level=logging.INFO):
    new_logger = logging.getLogger(logger_name)
    new_logger.handlers = []
    formatter = logging.Formatter(
            '[%(levelname)-8s] [%(name)-7s] %(message)s \t\t [%(asctime)s] (%(filename)s %(lineno)d %(name)s) (%('
            'threadName)s)')
    if log_file:
        file_handler = logging.FileHandler(log_file, mode="w")
        file_handler.setFormatter(formatter)
        new_logger.addHandler(file_handler)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    new_logger.addHandler(stream_handler)

    new_logger.setLevel(level)
    return new_logger


logger = setup_logger("GeneralDep")     # Deprecated: Replace with new ones
