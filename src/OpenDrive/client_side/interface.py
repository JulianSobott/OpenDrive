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
    :undoc-members:

public functions
-----------------

.. autofunction:: add_ignore_patterns_to_folder
.. autofunction:: add_sync_folder
.. autofunction:: get_all_remote_folders
.. autofunction:: get_sync_data
.. autofunction:: login_auto
.. autofunction:: login_manual
.. autofunction:: logout
.. autofunction:: register
.. autofunction:: remove_remote_folder
.. autofunction:: remove_synchronization
.. autofunction:: share_folder


"""
from typing import List, Tuple

from OpenDrive.client_side import authentication
from OpenDrive.client_side import file_changes_json
from OpenDrive.client_side import file_changes
from OpenDrive.client_side import merge_folders
from OpenDrive.general.paths import NormalizedPath
from OpenDrive import net_interface


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


def add_sync_folder(abs_local_path: NormalizedPath, remote_name: str,
                    include_regexes: List[str] = (".*",), exclude_regexes: List[str] = (),
                    merge_method: merge_folders.MergeMethod = merge_folders.MergeMethods.DEFAULT) -> Status:
    """Adds a synchronization between a local folder and a server folder. The content of both folders is merged,
    so that both folders are identical."""
    success = file_changes.add_folder(abs_local_path, include_regexes, exclude_regexes, remote_name)
    if not success:
        return Status.fail("Folder can not be added locally. It is nested in an existing folder or wraps "
                           "around an existing folder")
    new_added = net_interface.server.add_folder(remote_name)

    if new_added:
        merge_method = merge_folders.MergeMethods.TAKE_1

    status = merge_folders.merge_folders(abs_local_path, remote_name, merge_method)
    if not status.was_successful():
        return status

    return Status.success("Successfully added new sync folder pair.")


def remove_synchronization(abs_local_path: NormalizedPath) -> Status:
    """Stops the local folder from synchronizing with the remote folder. The remote folder is not deleted."""
    file_changes.remove_folder_from_watching(abs_local_path)
    return Status.success("Successfully removed folder from synchronization")


def remove_remote_folder(remote_name: NormalizedPath) -> Status:
    """Removes the remote folder, if it is not synchronized with any devices."""
    pass


def get_all_remote_folders(access_level=None) -> Tuple[Status, List[str]]:    # TODO: specify type hint
    """Returns a list with all folders that the user has access to."""
    if net_interface.ServerCommunicator.is_connected():
        return Status.success(""), net_interface.server.get_all_available_folders()
    else:
        return Status.fail("Cannot connect to server. Please ensure you are connected with the internet"), []


def get_sync_data() -> dict:
    """Returns a dict with all data specified in the changes.json file.
    All synced folders, include/exclude regular expressions.
    File changes."""
    return file_changes_json.get_all_data()


def share_folder(username: str, remote_name: str, permissions) -> Status:  # TODO: specify type hint permissions
    pass


def add_ignore_patterns_to_folder(patterns:List[str], abs_local_path: NormalizedPath) -> Status:
    pass





