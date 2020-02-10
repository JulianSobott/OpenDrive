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
from typing import Union, List

from OpenDrive.general.database import TableEntry, DBConnection
from OpenDrive.server_side import paths
from OpenDrive.general.database import Token


class Device(TableEntry):
    """
    :ivar device_id: Autoincrement id
    :ivar user_id: foreign_key
    :ivar mac_address: Unique for every device
    :ivar token: Allows auto login
    :ivar token_expires:
    """

    TABLE_NAME = "devices"
    DB_PATH = paths.SERVER_DB_PATH
    PRIMARY_KEY_NAME = "device_id"

    def __init__(self,
                 device_id: int,
                 user_id: int,
                 mac_address: str,
                 token: Union['Token', str],
                 token_expires: datetime.datetime) -> None:
        super().__init__()
        self._id = device_id
        self._user_id = user_id
        self._mac_address = mac_address
        if not isinstance(token, Token):
            token = Token.from_string(token)
        self._token = token
        self._token_expires = token_expires

    @staticmethod
    def create(user_id: int,
               mac_address: str,
               token: 'Token',
               token_expires: datetime.datetime) -> int:
        sql = "INSERT INTO `devices` (user_id, mac_address, token, token_expires) VALUES (?, ?, ?, ?)"
        with DBConnection(paths.SERVER_DB_PATH) as db:
            user_id = db.insert(sql, (user_id, mac_address, token.token, token_expires))
            return user_id

    """device_id"""

    @property
    def device_id(self) -> int:
        return self._id

    """user_id"""

    @property
    def user_id(self) -> int:
        return self._user_id

    """mac_address"""

    @property
    def mac_address(self) -> str:
        return self._mac_address

    @mac_address.setter
    def mac_address(self, val: str) -> None:
        self._change_field("mac_address", val)

    """token"""

    @property
    def token(self) -> 'Token':
        return self._token

    @token.setter
    def token(self, val: Union['Token', str]) -> None:
        if isinstance(val, Token):
            val = val.token
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

    @classmethod
    def get_by_user_id(cls, user_id: int) -> List['Device']:
        entries = cls.from_columns("user_id = ?", (user_id,))
        return entries

    def __repr__(self):
        return f"Device({self._id}, {self._user_id}, {self._mac_address}, {self._token}, {self._token_expires})"


