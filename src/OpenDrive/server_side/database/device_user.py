"""
:module: OpenDrive.server_side.database.device_user
:synopsis: DB class for the device_user table
:author: Julian Sobott

public classes
---------------

.. autoclass:: DeviceUser
    :exclude-members: DB_PATH
    :show-inheritance:
    :members:
    :inherited-members:
    :undoc-members:

"""
from typing import Optional

from OpenDrive.general.database import TableEntry, DBConnection
from OpenDrive.server_side import paths


class DeviceUser(TableEntry):
    """
    :ivar device_id:
    :ivar user_id:
    """

    TABLE_NAME = "device_user"
    DB_PATH = paths.SERVER_DB_PATH

    def __init__(self,
                 device_id: int,
                 user_id: int) -> None:
        super().__init__()
        self._device_id = device_id
        self._user_id = user_id

    @staticmethod
    def create(device_id: int,
               user_id: int) -> None:
        sql = "INSERT INTO `device_user` (device_id, user_id) VALUES (?, ?)"
        with DBConnection(paths.SERVER_DB_PATH) as db:
            db.insert(sql, (device_id, user_id))

    """device_id"""

    @property
    def device_id(self) -> int:
        return self._device_id

    """user_id"""

    @property
    def user_id(self) -> int:
        return self._user_id

    """Get by`s"""

    @classmethod
    def get_by_ids(cls, device_id: int, user_id: int) -> Optional['DeviceUser']:
        entries = cls.from_columns("device_id = ? AND user_id = ?", (device_id, user_id))
        assert len(entries) <= 1, "Non unique device_user in table 'device_user'!"
        if len(entries) == 0:
            return None
        device_user: DeviceUser = entries[0]
        return device_user

    def __repr__(self):
        return f"DeviceUser({self._device_id}, {self._user_id})"
