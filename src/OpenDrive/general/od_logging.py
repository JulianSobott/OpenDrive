"""
@author: Julian Sobott
@created: 13.11.2018


"""
import logging

MAX_MESSAGE_LEN = 1000
MIN_MESSAGE_LEN = 50

log_files_handlers = {}


def setup_logger(logger_name: str, log_file: str = None, level: int = logging.DEBUG):
    """Setup a new logger"""
    new_logger = logging.getLogger(logger_name)
    new_logger.handlers = []
    formatter = logging.Formatter(
            f'[%(levelname)-8s] [%(name)-8s] [%(asctime)s] %(message)-{MIN_MESSAGE_LEN}.{MAX_MESSAGE_LEN}s \t\t '
            f'(%(filename)s %(funcName)s %(lineno)d) (%('f'threadName)s)')
    if log_file:
        file_handler = log_files_handlers.setdefault(log_file, logging.FileHandler(log_file, mode="w"))
        file_handler.setFormatter(formatter)
        new_logger.addHandler(file_handler)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    new_logger.addHandler(stream_handler)

    new_logger.setLevel(level)
    return new_logger


def log_system(log_file):
    import sys
    import platform
    logger_system = setup_logger("System", log_file)
    logger_system.info(f"Python version: {sys.version}")
    logger_system.info(f"OS Info: platform={platform.platform()}, architecture={platform.architecture()}")


logger_database = setup_logger("Database")
