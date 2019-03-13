"""
@author: Julian Sobott

@brief: Interfaces between python and the db

@description:

classes:

    :class:`Change` (TableEntry):

    :class:`Ignore` (TableEntry):

    :class:`SyncFolder` (TableEntry):

functions:
    - :func:`create_database()` -> None:

@external_use:

@internal_use:
"""
import os
from datetime import datetime
from typing import Tuple, Optional, List

from OpenDrive.client_side import paths
from OpenDrive.general.database import DBConnection, TableEntry
from OpenDrive.general.paths import normalize_path
from OpenDrive.client_side.od_logging import logger


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
                             "ignore_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,"
                             "folder_id int not null references sync_folders(folder_id), "
                             "pattern VARCHAR(260) not null,"
                             "sub_folders int default 0"
                             ")")
        db.create(sql_table_ignores)


class Change(TableEntry):
    """Interface between python and DB change entry.
    call the static method `from_...()` to get a object, initialized with the values of the db.
    call the static method `create(...)` to insert a new change entry in the db.
    call the setter properties, to change the values in the db.
    """
    ACTION_PULL = (0, "PULL")
    ACTION_MOVE = (1, "MOVE")
    ACTION_DELETE = (2, "DELETE")

    _ACTIONS = {0: ACTION_PULL, 1: ACTION_MOVE, 2: ACTION_DELETE}

    TABLE_NAME = "changes"
    DB_PATH = paths.LOCAL_DB_PATH
    PRIMARY_KEY_NAME = "change_id"

    def __init__(self,
                 change_id: int,
                 folder_id: int,
                 current_rel_path: str,
                 is_folder: bool = False,
                 last_change_time_stamp: datetime = datetime.now(),
                 is_created: bool = False,
                 is_moved: bool = False,
                 is_deleted: bool = False,
                 is_modified: bool = False,
                 necessary_action: Tuple[int, str] = ACTION_PULL,
                 old_abs_path: Optional[str] = None
                 ) -> None:
        super().__init__()
        self._id = change_id
        self._folder_id: int = folder_id
        self._current_rel_path: str = normalize_path(current_rel_path)
        self._is_folder: bool = is_folder
        self._last_change_time_stamp: datetime = last_change_time_stamp
        self._is_created: bool = is_created
        self._is_moved: bool = is_moved
        self._is_deleted: bool = is_deleted
        self._is_modified: bool = is_modified
        if isinstance(necessary_action, int):
            necessary_action = self._ACTIONS[necessary_action]
        self._necessary_action: Tuple[int, str] = necessary_action
        if old_abs_path:
            old_abs_path = normalize_path(old_abs_path)
        self._old_abs_path: Optional[str] = old_abs_path

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
        current_rel_path = normalize_path(current_rel_path)
        if old_abs_path:
            old_abs_path = normalize_path(old_abs_path)
        with DBConnection(paths.LOCAL_DB_PATH) as db:
            return db.insert(sql, (folder_id, current_rel_path, is_folder, last_change_time_stamp, is_created, is_moved,
                                   is_deleted, is_modified, necessary_action[0], old_abs_path),
                             ignore_unique_error=True)
            # Hack: Ignore unique errors, because multiple entries can be created.
            # See `client_side/file_watcher/FileSystemEventHandler/on_any_event()` for more information

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
        new_path = normalize_path(new_path)
        self._change_field("current_rel_path", new_path)

    """is_folder"""
    @property
    def is_folder(self) -> bool:
        return bool(self._is_folder)

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
        return bool(self._is_created)

    @is_created.setter
    def is_created(self, new_value: bool):
        self._change_field("is_created", new_value)

    """is_moved"""
    @property
    def is_moved(self) -> bool:
        return bool(self._is_moved)

    @is_moved.setter
    def is_moved(self, new_value: bool):
        self._change_field("is_moved", new_value)

    """is_deleted"""
    @property
    def is_deleted(self) -> bool:
        return bool(self._is_deleted)

    @is_deleted.setter
    def is_deleted(self, new_value: bool):
        self._change_field("is_deleted", new_value)

    """is_modified"""
    @property
    def is_modified(self) -> bool:
        return bool(self._is_modified)

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
        if new_value:
            new_value = normalize_path(new_value)
        self._change_field("old_abs_path", new_value)

    @classmethod
    def get_possible_entry(cls, folder_id: int, current_rel_path: str) -> Optional['Change']:
        current_rel_path = normalize_path(current_rel_path)
        entries = cls.from_columns("folder_id=? and current_rel_path=?", (folder_id, current_rel_path))
        if len(entries) > 1:
            raise KeyError(f"To many entries with folder_id: {folder_id} and current_rel_path: {current_rel_path}")
        if len(entries) == 0:
            logger.info(f"No entry with folder_id: {folder_id} and current_rel_path: {current_rel_path}")
            return None
        change: Change = entries[0]
        return change

    @classmethod
    def get_all_folder_entries(cls, folder_id: int) -> List['Change']:
        entries: List['Change'] = cls.from_columns("folder_id=?", (folder_id,))
        return entries

    def __eq__(self, other):
        if not isinstance(other, Change):
            return False
        # Return True, when there are no differences in all __dict__
        try:
            return 0 == sum([1 if self.__dict__[key] != other.__dict__[key] else 0 for key in self.__dict__.keys()])
        except KeyError:
            return False


class Ignore(TableEntry):

    TABLE_NAME = "ignores"
    DB_PATH = paths.LOCAL_DB_PATH
    PRIMARY_KEY_NAME = "ignore_id"

    def __init__(self, ignore_id: int, folder_id: int, pattern: str, sub_folders: bool = True):
        super().__init__()
        self._id = ignore_id
        self._folder_id: int = folder_id
        self._pattern: str = pattern
        self._sub_folders: bool = sub_folders

    @staticmethod
    def create(folder_id: int, pattern: str, sub_folders: bool = True):
        sql = 'INSERT INTO "ignores" (' \
              '"folder_id", "pattern", "sub_folders") ' \
              'VALUES (?, ?, ?)'
        with DBConnection(paths.LOCAL_DB_PATH) as db:
            return db.insert(sql, (folder_id, pattern, sub_folders))

    """folder_id"""
    @property
    def folder_id(self) -> int:
        return self._folder_id

    @folder_id.setter
    def folder_id(self, new_value):
        self._change_field("folder_id", new_value)

    """pattern"""
    @property
    def pattern(self) -> str:
        return self._pattern

    @pattern.setter
    def pattern(self, new_value):
        self._change_field("pattern", new_value)

    """sub_folders"""
    @property
    def sub_folders(self) -> bool:
        return bool(self._sub_folders)

    @sub_folders.setter
    def sub_folders(self, new_value):
        self._change_field("sub_folders", new_value)


class SyncFolder(TableEntry):

    TABLE_NAME = "sync_folders"
    DB_PATH = paths.LOCAL_DB_PATH
    PRIMARY_KEY_NAME = "folder_id"

    def __init__(self, folder_id: int, abs_path: str):
        super().__init__()
        self._id = folder_id
        self._abs_path = normalize_path(abs_path)

    @classmethod
    def from_path(cls, abs_folder_path: str) -> 'SyncFolder':
        abs_folder_path = normalize_path(abs_folder_path)
        return cls._from_column("abs_path", abs_folder_path)

    @staticmethod
    def create(abs_path: str):
        abs_path = normalize_path(abs_path)
        sql = 'INSERT INTO "sync_folders" (' \
              '"abs_path") ' \
              'VALUES (?)'
        with DBConnection(paths.LOCAL_DB_PATH) as db:
            return db.insert(sql, (abs_path,))

    @property
    def abs_path(self) -> str:
        return self._abs_path

    @abs_path.setter
    def abs_path(self, new_path: str):
        new_path = normalize_path(new_path)
        self._change_field("abs_path", new_path)
