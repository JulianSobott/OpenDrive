"""
:module: OpenDrive.server_side.database.general
:synopsis: General DB functions at the server-side
:author: Julian Sobott

public classes
---------------

.. autoclass:: XXX
    :members:
    
public functions
-----------------

.. autofunction:: XXX

private classes
----------------

private functions
------------------

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
                             "`mac_address` VARCHAR(17) NOT NULL UNIQUE, "
                             "`token` VARCHAR(64) NOT NULL, "
                             "`token_expires` DATETIME)")
        db.create(sql_table_devices)

        sql_table_device_user = ("CREATE TABLE device_user ("
                                 "device_id INTEGER NOT NULL "
                                 "  REFERENCES devices,"
                                 "user_id   INTEGER NOT NULL "
                                 "  REFERENCES users, "
                                 "PRIMARY KEY (device_id, user_id) "
                                 ")")
        db.create(sql_table_device_user)
