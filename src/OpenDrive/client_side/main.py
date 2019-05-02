"""
:module: OpenDrive.client_side.main
:synopsis: Main script, that defines the execution order.
:author: Julian Sobott


public functions
----------------

.. autofunction:: start
.. autofunction:: mainloop
.. autofunction:: shutdown

private functions
-----------------


"""
import threading

from OpenDrive.client_side import file_changes as c_file_changes
from OpenDrive.client_side import net_start as c_net_start
from OpenDrive.client_side import interface as c_interface
from OpenDrive.client_side import synchronization as c_synchronization


def start():
    """Function that setups everything."""
    c_file_changes.start_observing()
    c_net_start.connect()
    status = c_interface.login_auto()
    if not status.was_successful():
        pass    # TODO: open gui login window
    c_synchronization.full_synchronize()
    mainloop()


def mainloop():
    while True:
        print("Waiting...")
        c_file_changes.sync_waiter.waiter.wait()
        c_file_changes.sync_waiter.waiter.clear()
        print("Synchronize")
        c_synchronization.full_synchronize()


def shutdown():
    c_net_start.close_connection()


if __name__ == '__main__':
    c_file_changes.start_observing()
    c_file_changes.add_folder(r"D:\Programmieren\OpenDrive\local\client_Side\DUMMY_FOLDER")
    mainloop()