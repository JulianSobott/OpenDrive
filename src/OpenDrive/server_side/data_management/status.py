"""
:module: OpenDrive.server_side.data_management.status
:synopsis: Status responses for calls to data management functions
:author: Julian Sobott

public classes
---------------

.. autoclass:: Status
    :members:

"""
from typing import NewType

ErrorCode = NewType("ErrorCode", int)
SUCCESS = ErrorCode(0)


class Status:

    def __init__(self, success: bool, message: str, error_code: ErrorCode):
        self._success = success
        self._message = message
        self._error_code = error_code

    @classmethod
    def fail(cls, message: str, error_code: ErrorCode) -> 'Status':
        return Status(success=False, message=message, error_code=error_code)

    @classmethod
    def success(cls, message: str) -> 'Status':
        return Status(success=True, message=message, error_code=SUCCESS)

    def was_successful(self) -> bool:
        return self._success

    def get_message(self) -> str:
        return self._message

    def get_error_code(self) -> int:
        return self._error_code

    def __bool__(self):
        return self._success

    def __repr__(self):
        return f"Status(success={self._success}, text='{self._message}', error_code={self._error_code}"
