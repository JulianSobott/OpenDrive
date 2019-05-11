"""
:module: OpenDrive.client_side.interface
:synopsis: Interface between the gui/ui and the backend
:author: Julian Sobott

This module does not contain any logic. It only defines the signatures of the interface functions. All functions are
forwarded to the proper modules.

public classes
---------------

.. autoclass:: Status
    :members:

public functions
-----------------

.. autofunction:: add_ignore_patterns_to_folder
.. autofunction:: add_sync_folder
.. autofunction:: get_all_remote_folders
.. autofunction:: get_all_sync_folder_pairs
.. autofunction:: login_auto
.. autofunction:: login_manual
.. autofunction:: logout
.. autofunction:: register
.. autofunction:: remove_remote_folder
.. autofunction:: remove_synchronization
.. autofunction:: share_folder


"""
from typing import List

from OpenDrive.general.device_data import get_mac
from OpenDrive.net_interface import server
from OpenDrive.client_side import authentication


class Status:
    """Data class that is used to transmit status messages from the backend to the ui."""

    def __init__(self, success: bool, text: str, error_code: int = -1):
        self._success = success
        self._text = text
        self._error_code = error_code

    @classmethod
    def fail(cls, text: str, error_code: int = -1) -> 'Status':
        return Status(success=False, text=text, error_code=error_code)

    @classmethod
    def success(cls, text: str) -> 'Status':
        return Status(success=True, text=text)

    def was_successful(self) -> bool:
        return self._success

    def get_text(self) -> str:
        return self._text

    def get_error_code(self) -> int:
        return self._error_code

    def __repr__(self):
        return f"Status(success={self._success}, text='{self._text}', error_code={self._error_code}"


def register(username: str, password: str, email: str = None) -> Status:
    return authentication.register_user_device(username, password, email)


def login_auto() -> Status:
    """Try to auto login with a previously stored token. Returns the success status."""
    return authentication.login_auto()


def login_manual(username: str, password: str, allow_auto_login=True) -> Status:
    return authentication.login_manual(username, password, allow_auto_login)


def logout() -> Status:
    return authentication.logout()


def add_sync_folder(abs_local_path: str, remote_name: str) -> Status:
    pass


def remove_synchronization(abs_local_path: str) -> Status:
    """Stops the local folder from synchronizing with the remote folder. The remote folder is not deleted."""
    pass


def remove_remote_folder(remote_name) -> Status:
    """Removes the remote folder, if it is not synchronized with any devices."""
    pass


def get_all_remote_folders(access_level=None) -> list:    # TODO: specify type hint
    """Returns a list with all folders that the user has access to."""
    pass


def get_all_sync_folder_pairs() -> list:  # TODO: specify type hint
    pass


def share_folder(username: str, remote_name: str, permissions) -> Status:  # TODO: specify type hint permissions
    pass


def add_ignore_patterns_to_folder(patterns:List[str], abs_local_path) -> Status:
    pass





