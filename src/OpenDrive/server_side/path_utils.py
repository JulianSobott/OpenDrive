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
from OpenDrive import net_interface
from OpenDrive.server_side import paths


def rel_user_path_to_abs(rel_path: str, user_id: int = -1):
    if user_id == -1:
        user_id = net_interface.get_user_id()
    return paths.normalize_path(get_users_root_folder(user_id), rel_path)


def get_users_root_folder(user_id: int) -> str:
    return paths.normalize_path(paths.FOLDERS_ROOT, f"user_{user_id}/")