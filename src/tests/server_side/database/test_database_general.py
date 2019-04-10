"""
:module:
:synopsis:
:author: Julian Sobott

"""
import unittest
import os

from OpenDrive.server_side import database, paths
from OpenDrive.general.database import delete_db_file
from OpenDrive.general.paths import normalize_path
from tests.od_logging import logger


class TestDatabaseConnections(unittest.TestCase):

    def test_create_database_non_existing(self):
        delete_db_file(paths.SERVER_DB_PATH)
        database.create_database()
        self.assertTrue(os.path.exists(paths.SERVER_DB_PATH),
                        "Database file was not created or created at the wrong place!")

    def test_tables_creation(self):
        delete_db_file(paths.SERVER_DB_PATH)
        database.create_database()
        sql = "SELECT name  FROM sqlite_master WHERE type='table'"
        with database.DBConnection(paths.SERVER_DB_PATH) as db:
            ret = db.get(sql)
        tables = [table_name for table_name, in ret]
        self.assertTrue("users" in tables)
        self.assertTrue("devices" in tables)
        self.assertTrue("device_user" in tables)
        self.assertTrue("folders" in tables)

