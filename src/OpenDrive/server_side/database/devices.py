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
                 token: str) -> None:
        super().__init__()
        self._id = device_id
        self._mac_address = mac_address
        self._token = token

    @staticmethod
    def create(mac_address: str,
               token: str) -> int:
        sql = "INSERT INTO `devices` (mac_address, token) VALUES (?, ?)"
        with DBConnection(paths.SERVER_DB_PATH) as db:
            user_id = db.insert(sql, (mac_address, token))
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

    """Get by`s"""

    def __repr__(self):
        return f"Device({self._id}, {self._mac_address}, {self._token})"

