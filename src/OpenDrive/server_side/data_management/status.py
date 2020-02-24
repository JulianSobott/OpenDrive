"""
:module: OpenDrive.server_side.data_management.status
:synopsis: Status responses for calls to data management functions
:author: Julian Sobott

public classes
---------------

.. autoclass:: Status
    :members:

"""
from typing import NewType, Any, TypeVar, Generic, Tuple

ErrorCode = NewType("ErrorCode", Tuple[int, str])
SUCCESS = ErrorCode((0, "SUCCESS"))

T = TypeVar("T")


class Status(Generic[T]):

    def __init__(self, success: bool, data: T, error_code: ErrorCode):
        self._success = success
        self.data = data
        self.error_code = error_code

    @classmethod
    def fail(cls, error_code: ErrorCode) -> 'Status':
        return Status(success=False, data=None, error_code=error_code)

    @classmethod
    def success(cls, data: T) -> 'Status':
        return Status(success=True, data=data, error_code=SUCCESS)

    def was_successful(self) -> bool:
        return self._success

    def __bool__(self):
        return self._success

    def __repr__(self):
        return f"Status(success={self._success}, text='{self.data}', error_code={self.error_code}"
