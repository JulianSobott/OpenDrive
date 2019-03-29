"""
:module: OpenDrive.server_side.database.devices
:synopsis: DB class for the devices table
:author: Julian Sobott

public classes
---------------

.. autoclass:: Device
    :exclude-members: DB_PATH
    :show-inheritance:
    :members:
    :inherited-members:
    :undoc-members:

"""
import datetime
from typing import Optional

from OpenDrive.general.database import TableEntry, DBConnection
from OpenDrive.server_side import paths


class Device(TableEntry):
    """
    :ivar device_id: Autoincrement id
    :ivar mac_address: Unique for every device
    :ivar token: Allows auto login. Integrated timestamp when expires
    """

    TABLE_NAME = "devices"
    DB_PATH = paths.SERVER_DB_PATH
    PRIMARY_KEY_NAME = "device_id"

    def __init__(self,
                 device_id: int,
                 mac_address: str,
                 token: str,
                 token_expires: datetime.datetime) -> None:
        super().__init__()
        self._id = device_id
        self._mac_address = mac_address
        self._token = token
        self._token_expires = token_expires

    @staticmethod
    def create(mac_address: str,
               token: str,
               token_expires: datetime.datetime) -> int:
        sql = "INSERT INTO `devices` (mac_address, token, token_expires) VALUES (?, ?, ?)"
        with DBConnection(paths.SERVER_DB_PATH) as db:
            user_id = db.insert(sql, (mac_address, token, token_expires))
            return user_id

    """user_id"""

    @property
    def device_id(self) -> int:
        return self._id

    """mac_address"""

    @property
    def mac_address(self) -> str:
        return self._mac_address

    @mac_address.setter
    def mac_address(self, val: str) -> None:
        self._change_field("mac_address", val)

    """token"""

    @property
    def token(self) -> str:
        return self._token

    @token.setter
    def token(self, val: str) -> None:
        self._change_field("token", val)

    """token_expires"""

    @property
    def token_expires(self) -> datetime.datetime:
        return self._token_expires

    @token_expires.setter
    def token_expires(self, val: datetime.datetime) -> None:
        self._change_field("token_expires", val)

    """Get by`s"""
    @classmethod
    def get_by_mac(cls, mac_address: str):
        entries = cls.from_columns("mac_address = ?", (mac_address,))
        assert len(entries) <= 1, "Non unique mac_address in table 'devices'!"
        if len(entries) == 0:
            return None
        device: Device = entries[0]
        return device

    def __repr__(self):
        return f"Device({self._id}, {self._mac_address}, {self._token})"


class Token:

    @staticmethod
    def generate_token(length: Optional[int]=None):
        pass

    @staticmethod
    def is_token_expired(date):
        pass
