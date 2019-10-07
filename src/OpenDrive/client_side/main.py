"""
:module: OpenDrive.client_side.main
:synopsis: Main script, that defines the execution order.
:author: Julian Sobott


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

from OpenDrive.client_side import file_changes as c_file_changes
from OpenDrive.client_side import net_start as c_net_start
from OpenDrive.client_side import interface as c_interface
from OpenDrive.client_side import synchronization as c_synchronization
from OpenDrive.client_side import file_changes_json as c_json
from OpenDrive.client_side.od_logging import logger
from OpenDrive.client_side.gui import tray


MIN_UPDATE_PAUSE_TIME = 5
"""After a call to sync appears the program waits for this time, to prevent too frequent update rates."""

is_on_event = threading.Event()


def start():
    """Function that setups everything."""
    def wrapper():
        c_json.init_file()
        c_file_changes.start_observing()
        c_file_changes.sync_waiter.waiter.clear()
        c_net_start.connect()
        status = c_interface.login_auto()
        c_synchronization.full_synchronize()
        is_on_event.set()
        mainloop()
    tray.start_tray(wrapper)


def mainloop():
    while is_on_event.is_set():
        logger.info("Waiting... for changes")
        c_file_changes.sync_waiter.waiter.wait()
        if is_on_event.is_set():
            time.sleep(MIN_UPDATE_PAUSE_TIME)
            c_file_changes.sync_waiter.waiter.clear()
            logger.info("Synchronizing")
            c_synchronization.full_synchronize()


def shutdown():
    is_on_event.clear()
    c_file_changes.sync_waiter.waiter.set()
    c_file_changes.stop_observing()
    c_net_start.close_connection()


if __name__ == '__main__':
    start()
