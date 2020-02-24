"""
:module: OpenDrive.server_side.file_management.user
:synopsis: Handling user data
:author: Julian Sobott

public functions
----------------

.. autofunction:: authenticate_user

private functions
-----------------


"""
from OpenDrive.server_side.data_management.status import Status, ErrorCode

_USER_ERROR_CODE = 100

WRONG_PASSWORD = ErrorCode(_USER_ERROR_CODE | 1)


def authenticate_user(username: str, password_hash: str) -> Status:
    """
    Authentication of a user

    parameters
    ----------
    username: str
    password_hash: str

    return
    ------
    Status
        SUCCESS if the hash is the same as the stored one
        WRONG_PASSWORD otherwise
    """

