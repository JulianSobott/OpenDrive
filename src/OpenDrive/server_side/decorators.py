"""
:module: OpenDrive.
:synopsis: 
:author: Julian Sobott

public classes
---------------

.. autoclass:: XXX
    :members:


public functions
----------------

.. autofunction:: XXX

private functions
-----------------


"""
import functools
import time

from OpenDrive import net_interface
from OpenDrive.server_side.od_logging import client_logger_security


def requires_authentication(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        user = net_interface.get_user()
        if not user.is_authenticated:
            client_logger_security().info(f"User is not authenticated to execute this function: "
                                          f"user={user}, function={func.__name__}")
        while not user.is_authenticated:
            # TODO: Maybe add max counter. Care to not crash the client program, because it expects a valid return
            net_interface.get_user().remote_functions.open_authentication_window()
            if not user.is_authenticated:
                client_logger_security().debug(f"User is still not authenticated! user={user}, "
                                               f"function={func.__name__}")
            time.sleep(1)  # TODO: add better way instead of sleep for create all files and setup all users stuff
        return func(*args, **kwargs)
    return wrapper
