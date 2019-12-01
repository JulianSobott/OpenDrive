"""
:module: OpenDrive.client_side.main
:synopsis: Main script, that defines the execution order.
:author: Julian Sobott

## TODO:
- proper shutdown
- possible to close gui
- offline gui

public functions
----------------

.. autofunction:: mainloop
.. autofunction:: shutdown
.. autofunction:: start

private members
-----------------

.. autodata:: MIN_UPDATE_PAUSE_TIME

"""
import time
import threading
import pyprofiling

from OpenDrive.client_side import file_changes as c_file_changes
from OpenDrive.client_side import net_start as c_net_start
from OpenDrive.client_side import interface as c_interface
from OpenDrive.client_side import synchronization as c_synchronization
from OpenDrive.client_side import file_changes_json as c_json
from OpenDrive.client_side.od_logging import logger_general, init_logging
from OpenDrive.client_side.gui import tray
from OpenDrive.client_side import gui


MIN_UPDATE_PAUSE_TIME = 5
"""After a call to sync appears the program waits for this time, to prevent too frequent update rates."""

is_on_event = threading.Event()


def start():
    """Function that setups everything."""
    init_logging()
    logger_general.info("Start main application")

    def wrapper():
        global is_on_event
        is_on_event.set()
        c_json.init_file()
        c_file_changes.start_observing()
        c_file_changes.sync_waiter.waiter.clear()
        logger_general.info("Start connecting to server")
        while is_on_event.is_set() and not c_net_start.connect(timeout=60):
            # TODO: Add server info (IP:PORT)
            sleep_time = 1
            time.sleep(sleep_time)
        if is_on_event.is_set():
            gui.main.main(authentication_only=True, try_auto_login=True)
        if is_on_event.is_set():
            c_synchronization.full_synchronize()
        if is_on_event.is_set():
            mainloop()
    logger_general.info("Start tray")
    tray.start_tray(wrapper, shutdown)


@pyprofiling.stop_in_seconds(5)
def mainloop():
    logger_general.info("Start mainloop")
    while is_on_event.is_set():
        logger_general.info("Waiting for changes")
        c_file_changes.sync_waiter.waiter.wait()
        if is_on_event.is_set():
            time.sleep(MIN_UPDATE_PAUSE_TIME)
            c_file_changes.sync_waiter.waiter.clear()
            logger_general.info("Full synchronize")
            c_synchronization.full_synchronize()


def shutdown():
    global is_on_event
    logger_general.info("Start shutdown main program")
    is_on_event.clear()
    c_file_changes.sync_waiter.waiter.set()
    try:
        c_file_changes.stop_observing()
    except RuntimeError:
        pass    # already stopped
    try:
        c_net_start.close_connection()
    except RuntimeError:
        pass    # already stopped
    try:
        gui.main.stop()
    except RuntimeError:
        pass    # already stopped
    logger_general.info("Finished shutdown main program")


if __name__ == '__main__':
    start()
