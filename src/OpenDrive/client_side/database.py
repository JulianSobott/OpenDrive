"""
@author: Julian Sobott
@brief:
@description:

@external_use:

@internal_use:
"""
import os
from datetime import datetime
from typing import Tuple, Optional

from OpenDrive.client_side import paths
from OpenDrive.general.database import DBConnection


def create_database() -> None:
    """Create the DB with all tables."""
    if os.path.exists(paths.LOCAL_DB_PATH):
        raise FileExistsError("Cannot create new db, because it already exists!")
    with DBConnection(paths.LOCAL_DB_PATH) as db:
        sql_table_sync_folders = ("CREATE TABLE sync_folders ("
                                  "`folder_id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,"
                                  "`abs_path` VARCHAR(260) NOT NULL UNIQUE)")
        db.create(sql_table_sync_folders)
        sql_table_changes = ("CREATE TABLE changes ("
                             "change_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT ,"
                             "folder_id INT NOT NULL,"
                             "current_rel_path VARCHAR(260) NOT NULL UNIQUE,"
                             "is_folder INT NOT NULL ,"
                             "last_change_time_stamp DATETIME DEFAULT CURRENT_TIMESTAMP,"
                             "is_created INT DEFAULT 0,"
                             "is_moved INT DEFAULT 0,"
                             "is_deleted INT DEFAULT 0,"
                             "is_modified INT DEFAULT 0,"
                             "necessary_action INT,"
                             "old_abs_path VARCHAR(260) UNIQUE,"
                             "FOREIGN KEY (folder_id) REFERENCES sync_folders(folder_id)"
                             ")")
        db.create(sql_table_changes)
        sql_table_ignores = ("create table ignores("
                             "ignore_id int primary key,"
                             "folder_id int not null references sync_folders(folder_id), "
                             "pattern VARCHAR(260) not null,"
                             "sub_folders int default 0"
                             ")")
        db.create(sql_table_ignores)


class Change:
    """Interface between python and DB change entry.
    call the `__init__(change_id)` to get a object, initialized with the values of the db.
    call the static method `create(...)` to insert a new change entry in the db.
    call the setter properties, to change the values in the db.
    """
    ACTION_PULL = (0, "PULL")
    ACTION_MOVE = (1, "MOVE")
    ACTION_DELETE = (2, "DELETE")

    def __init__(self, change_id: int):
        """A object with all db values of the change_id is initialized. Raises KeyError if no entry exists."""
        sql = "SELECT * FROM changes WHERE change_id = ?"
        with DBConnection(paths.LOCAL_DB_PATH) as db:
            ret = db.get(sql, (change_id,))
        if len(ret) == 0:
            raise KeyError(f"No change entry in 'changes' with id {change_id}!")
        values = ret[0]
        self.id = change_id
        self._folder_id: int = values[1]
        self._current_rel_path: str = values[2]
        self._is_folder: bool = values[3]
        self._last_change_time_stamp: datetime = values[4]
        self._is_created: bool = values[5]
        self._is_moved: bool = values[6]
        self._is_deleted: bool = values[7]
        self._is_modified: bool = values[8]
        self._necessary_action: Tuple[int, str] = values[9]
        self._old_abs_path: Optional[str] = values[10]

    @staticmethod
    def create(folder_id: int,
               current_rel_path: str,
               is_folder: bool = False,
               last_change_time_stamp: datetime = datetime.now(),
               is_created: bool = False,
               is_moved: bool = False,
               is_deleted: bool = False,
               is_modified: bool = False,
               necessary_action: Tuple[int, str] = ACTION_PULL,
               old_abs_path: Optional[str] = None) -> int:
        """Insert a new entry to the db"""
        assert isinstance(folder_id, int)
        assert isinstance(current_rel_path, str)
        assert 0 <= necessary_action[0] <= 2

        sql = 'INSERT INTO "changes" (' \
              '"folder_id", "current_rel_path", "is_folder", "last_change_time_stamp", "is_created", "is_moved", ' \
              '"is_deleted", "is_modified", "necessary_action", "old_abs_path") ' \
              'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
        with DBConnection(paths.LOCAL_DB_PATH) as db:
            return db.insert(sql, (folder_id, current_rel_path, is_folder, last_change_time_stamp, is_created, is_moved,
                                   is_deleted, is_modified, necessary_action[0], old_abs_path))

    """folder_id"""
    @property
    def folder_id(self) -> int:
        return self._folder_id

    @folder_id.setter
    def folder_id(self, new_id: int):
        self._change_field("folder_id", new_id)

    """current_rel_path"""
    @property
    def current_rel_path(self) -> str:
        return self._current_rel_path

    @current_rel_path.setter
    def current_rel_path(self, new_path: str):
        self._change_field("current_rel_path", new_path)

    """is_folder"""
    @property
    def is_folder(self) -> bool:
        return self._is_folder

    @is_folder.setter
    def is_folder(self, new_value: bool):
        self._change_field("is_folder", new_value)

    """last_change_time_stamp"""
    @property
    def last_change_time_stamp(self) -> datetime:
        return self._last_change_time_stamp

    @last_change_time_stamp.setter
    def last_change_time_stamp(self, new_value: datetime):
        self._change_field("last_change_time_stamp", new_value)

    """is_created"""

    @property
    def is_created(self) -> bool:
        return self._is_created

    @is_created.setter
    def is_created(self, new_value: bool):
        self._change_field("is_created", new_value)

    """is_moved"""
    @property
    def is_moved(self) -> bool:
        return self._is_moved

    @is_moved.setter
    def is_moved(self, new_value: bool):
        self._change_field("is_moved", new_value)

    """is_deleted"""
    @property
    def is_deleted(self) -> bool:
        return self._is_deleted

    @is_deleted.setter
    def is_deleted(self, new_value: bool):
        self._change_field("is_deleted", new_value)

    """is_modified"""
    @property
    def is_modified(self) -> bool:
        return self._is_modified

    @is_modified.setter
    def is_modified(self, new_value: bool):
        self._change_field("is_modified", new_value)

    """necessary_action"""
    @property
    def necessary_action(self) -> Tuple[int, str]:
        return self._necessary_action

    @necessary_action.setter
    def necessary_action(self, new_value: Tuple[int, str]):
        self._change_field("necessary_action", new_value)

    """old_abs_path"""
    @property
    def old_abs_path(self) -> Optional[str]:
        return self._old_abs_path

    @old_abs_path.setter
    def old_abs_path(self, new_value: Optional[str]):
        self._change_field("old_abs_path", new_value)

    def _change_field(self, field_name: str, new_value) -> None:
        if ";" in field_name or ")" in field_name:
            raise ValueError("Preventing possible sql injection")
        sql = f'UPDATE "changes" SET {field_name} = ? WHERE "change_id" = ?'
        with DBConnection(paths.LOCAL_DB_PATH) as db:
            db.update(sql, (new_value, self.id))

