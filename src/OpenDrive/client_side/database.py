"""
@author: Julian Sobott
@brief:
@description:

@external_use:

@internal_use:
"""
import os

from OpenDrive.client_side import paths
from OpenDrive.general.database import DBConnection


def create_database() -> None:
    """Create the DB with all tables."""
    if os.path.exists(paths.LOCAL_DB_PATH):
        raise FileExistsError("Cannot create new db, because it already exists!")
    with DBConnection(paths.LOCAL_DB_PATH) as db:
        sql_table_sync_folders = ("CREATE TABLE sync_folders ("
                                  "`folder_id` INT NOT NULL PRIMARY KEY ,"
                                  "`abs_path` VARCHAR(260) NOT NULL UNIQUE)")
        db.create(sql_table_sync_folders)
        sql_table_changes = ("CREATE TABLE changes ("
                             "change_id INT NOT NULL PRIMARY KEY,"
                             "folder_id INT NOT NULL,"
                             "current_rel_path VARCHAR(260) NOT NULL UNIQUE,"
                             "is_folder INT NOT NULL ,"
                             "last_change_time_stamp TEXT NOT NULL ,"
                             "is_created INT DEFAULT 0,"
                             "is_moved INT DEFAULT 0,"
                             "is_deleted INT DEFAULT 0,"
                             "is_modified INT DEFAULT 0,"
                             "necessary_action INT,"
                             "old_abs_path VARCHAR(260) NOT NULL UNIQUE,"
                             "FOREIGN KEY (folder_id) REFERENCES sync_folders(folder_id)"
                             ")")
        db.create(sql_table_changes)
