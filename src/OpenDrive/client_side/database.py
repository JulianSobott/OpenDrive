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


class ChangesTable:
    ACTION_PULL = (0, "PULL")
    ACTION_MOVE = (1, "MOVE")
    ACTION_DELETE = (2, "DELETE")

    @staticmethod
    def insert(folder_id: int,
               current_rel_path: str,
               is_folder: bool = False,
               last_change_time_stamp: datetime = datetime.now(),
               is_created: bool = False,
               is_moved: bool = False,
               is_deleted: bool = False,
               is_modified: bool = False,
               necessary_action: Tuple[int, str] = ACTION_PULL,
               old_abs_path: Optional[str] = None):
        sql = 'INSERT INTO "changes" (' \
              '"folder_id", "current_rel_path", "is_folder", "last_change_time_stamp", "is_created", "is_moved", ' \
              '"is_deleted", "is_modified", "necessary_action", "old_abs_path") ' \
              'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
        assert isinstance(folder_id, int)
        assert isinstance(current_rel_path, str)
        assert 0 <= necessary_action[0] <= 2

        with DBConnection(paths.LOCAL_DB_PATH) as db:
            db.insert(sql, (folder_id, current_rel_path, is_folder, last_change_time_stamp, is_created, is_moved,
                            is_deleted, is_modified, necessary_action[0], old_abs_path))
