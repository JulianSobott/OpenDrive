"""
:module: OpenDrive.client_side.main
:synopsis: Main script, that defines the execution order.
:author: Julian Sobott

## TODO:
- proper shutdown
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

from OpenDrive.client_side import file_changes as c_file_changes
from OpenDrive.client_side import net_start as c_net_start
from OpenDrive.client_side import synchronization as c_synchronization
from OpenDrive.client_side import file_changes_json as c_json
from OpenDrive.client_side.od_logging import logger_general, init_logging
from OpenDrive.client_side.gui import tray
from OpenDrive.client_side import gui
from OpenDrive.client_side.gui import authentication
from OpenDrive.client_side import program_state

MIN_UPDATE_PAUSE_TIME = 5
"""After a call to sync appears the program waits for this time, to prevent too frequent update rates."""


def start():
    """Function that setups everything."""
    init_logging()
    logger_general.info("Start main application")
    program_state.program.started()
    gui.start_gui_thread()

    def wrapper():
        c_json.init_file()
        c_file_changes.start_observing()
        c_file_changes.sync_waiter.waiter.clear()
        logger_general.info("Start connecting to server")
        while program_state.program.is_running() and not c_net_start.connect(timeout=60):
            # connect till connected
            sleep_time = 1
            time.sleep(sleep_time)
        if program_state.program.is_running():
            logger_general.info("Start authentication at server: Trying `auto login` fallback `manual login`")
            authentication.authenticate_only()
        program_state.is_authenticated_at_server.wait_till_running()
        if program_state.program.is_running():
            c_synchronization.full_synchronize()
        if program_state.program.is_running():
            mainloop()
    logger_general.info("Start tray")
    tray.start_tray(wrapper, shutdown)


def mainloop():
    logger_general.info("Start mainloop")
    while program_state.program.is_running():
        logger_general.info("Waiting for changes")
        c_file_changes.sync_waiter.waiter.wait()
        if program_state.program.is_running():
            time.sleep(MIN_UPDATE_PAUSE_TIME)
            c_file_changes.sync_waiter.waiter.clear()
            logger_general.info("Full synchronize")
            c_synchronization.full_synchronize()


def shutdown():
    logger_general.info("Start shutdown main program")
    c_file_changes.sync_waiter.waiter.set()
    try:
        c_file_changes.stop_observing()
    except RuntimeError:
        pass    # already stopped
    try:
        c_net_start.close_connection()
    except RuntimeError:
        pass    # already stopped
    gui.stop()
    program_state.program.stopped()
    logger_general.info("Finished shutdown main program")


if __name__ == '__main__':
    start()
