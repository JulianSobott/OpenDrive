"""
:module: OpenDrive.server_side.database.folders
:synopsis: DB class for the folders table
:author: Julian Sobott

public classes
---------------

.. autoclass:: Folder
    :exclude-members: DB_PATH
    :show-inheritance:
    :members:
    :inherited-members:
    :undoc-members:

"""
from typing import Optional

from OpenDrive.general.database import TableEntry, DBConnection
from OpenDrive.server_side import paths


class Folder(TableEntry):
    """
    :ivar folder_id:
    :ivar user_id:
    :ivar folder_name:
    """

    TABLE_NAME = "folders"
    DB_PATH = paths.SERVER_DB_PATH
    PRIMARY_KEY_NAME = "folder_id"

    def __init__(self,
                 folder_id: int,
                 user_id: int,
                 folder_name: str) -> None:
        super().__init__()
        self._id = folder_id
        self._user_id = user_id
        self._folder_name = folder_name

    @staticmethod
    def create(user_id: int,
               folder_name: str) -> int:
        sql = "INSERT INTO `folders` (user_id, folder_name) VALUES (?, ?)"
        with DBConnection(paths.SERVER_DB_PATH) as db:
            folder_id = db.insert(sql, (user_id, folder_name))
            return folder_id

    """folder_id"""

    @property
    def folder_id(self) -> int:
        return self._id

    """user_id"""

    @property
    def user_id(self) -> int:
        return self._user_id

    @user_id.setter
    def user_id(self, val: int) -> None:
        self._change_field("user_id", val)

    """folder_name"""

    @property
    def folder_name(self) -> str:
        return self._folder_name

    @folder_name.setter
    def folder_name(self, val: str) -> None:
        self._change_field("folder_name", val)

    """Get by`s"""

    @classmethod
    def get_by_user_and_name(cls, user_id: int, folder_name: str) -> Optional['Folder']:
        entries = cls.from_columns("user_id = ? and folder_name = ?", (user_id, folder_name))
        assert len(entries) <= 1, "Non unique folder in table 'folders'!"
        if len(entries) == 0:
            return None
        folder: Folder = entries[0]
        return folder

    def __repr__(self):
        return f"User({self._id}, {self._user_id}, {self._folder_name})"
