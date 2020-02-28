"""
:module: OpenDrive.server_side.database.general
:synopsis: General DB functions at the server-side
:author: Julian Sobott

public functions
-----------------

.. autofunction:: create_database


"""
import os

from OpenDrive.server_side import paths
from OpenDrive.general.database import DBConnection


def create_database() -> None:
    """Create the DB with all tables."""
    if os.path.exists(paths.SERVER_DB_PATH):
        raise FileExistsError("Cannot create new db, because it already exists!")
    with DBConnection(paths.SERVER_DB_PATH) as db:
        sql_table_users = ("CREATE TABLE users ("
                           "`user_id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, "
                           "`username` VARCHAR(30) NOT NULL UNIQUE, "
                           "`password` VARCHAR(96) NOT NULL, "
                           "`email` VARCHAR(40))")
        db.create(sql_table_users)

        sql_table_devices = ("CREATE TABLE devices ("
                             "`device_id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, "
                             "user_id   INTEGER NOT NULL "
                             "  REFERENCES users, "
                             "`mac_address` VARCHAR(17) NOT NULL UNIQUE, "
                             "`token` VARCHAR(64) NOT NULL, "
                             "`token_expires` DATETIME)")
        db.create(sql_table_devices)

        sql_table_folders = ("CREATE TABLE folders ("
                             "folder_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, "
                             "user_id   INTEGER NOT NULL "
                             "  REFERENCES users, "
                             "folder_name VARCHAR(100) "
                             ")")
        db.create(sql_table_folders)

        sql_table_user_device = ("CREATE TABLE user_device ("
                                 "device_id INTEGER REFERENCES devices(device_id),"
                                 "user_id INTEGER REFERENCES users(user_id),"
                                 "PRIMARY KEY (device_id, user_id))")
        db.create(sql_table_user_device)
