"""
@author: Julian Sobott
@brief:
@description:

@external_use:

@internal_use:
"""
import sqlite3
import os

from OpenDrive.client_side import paths


def create_database() -> None:
    """Create the DB with all tables."""
    if os.path.exists(paths.LOCAL_DB_PATH):
        raise FileExistsError("Cannot create new db, because it already exists!")
    with DBConnection() as db:
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


class DBConnection:

    def __init__(self) -> None:
        self.connection: sqlite3.Connection
        self.cursor: sqlite3.Cursor

    def __enter__(self) -> 'DBConnection':
        self.connection = sqlite3.connect(paths.LOCAL_DB_PATH)
        self.cursor = self.connection.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()

    def get(self, sql: str, args: tuple = ()) -> list:
        self.cursor.execute(sql, args)
        return self.cursor.fetchall()

    def create(self, sql: str, args: tuple = ()) -> None:
        self.cursor.execute(sql, args)

    def insert(self, sql: str, args: tuple = ()) -> int:
        self.cursor.execute(sql, args)
        return self.cursor.lastrowid

    def update(self, sql: str, args: tuple = ()) -> None:
        self.cursor.execute(sql, args)

    def delete(self, sql: str, args: tuple = ()) -> None:
        self.cursor.execute(sql, args)
