"""
:module: OpenDrive.client_side.gui.authentication.authentication
:synopsis: authenticating the user
:author: Julian Sobott

public functions
----------------

.. autofunction:: authenticate

private functions
-----------------

"""
from OpenDrive.client_side.authentication import login_auto
from OpenDrive.client_side.od_logging import logger_gui, logger_security
from OpenDrive.client_side import gui


def authenticate_only():
    """Try every possible options to authenticate the user at the server."""
    status = login_auto()
    if not status.was_successful():
        gui.open_gui(authentication_only=True)
    else:
        pass
