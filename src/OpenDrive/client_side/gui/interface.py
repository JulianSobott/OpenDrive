"""
:module: OpenDrive.client_side.gui.interface
:synopsis: Interface between the backend and the gui
:author: Julian Sobott

This module does not contain any logic. It only defines the signatures of the interface functions. All functions are
forwarded to the proper modules.

public classes
---------------

.. autoclass:: SynchronizationStatus
    :members:
    :undoc-members:

public functions
-----------------

..autofunction:: set_sync_status_of_folder
"""


class SynchronizationStatus:
    #: no local changes, no remote changes
    SYNCED = "synced"
    #: synced but there were conflicts
    MERGE_CONFLICTS = "merge_conflicts"
    # currently syncing
    SYNCING = "syncing"
    # local changes that are not synced with the server
    NOT_SYNCED_LOCAL_CHANGES = "not_synced_local_changes"
    # remote changes that are not synced with this device
    NOT_SYNCED_REMOTE_CHANGES = "not_synced_remote_changes"


def set_sync_status_of_folder(folder, status: SynchronizationStatus) -> None:
    """Request to update the synchronization status of the given folder.
    """
    pass
