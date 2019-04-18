"""
:module:
:synopsis:
:author: Julian Sobott

"""
import unittest
import os

from OpenDrive.server_side import database, paths as server_paths
from tests.server_side.database.helper_database import h_setup_server_database


class TestDatabaseConnections(unittest.TestCase):

    def setUp(self) -> None:
        h_setup_server_database()

    def test_create_database_non_existing(self):
        self.assertTrue(os.path.exists(server_paths.SERVER_DB_PATH),
                        "Database file was not created or created at the wrong place!")

    def test_tables_creation(self):
        sql = "SELECT name  FROM sqlite_master WHERE type='table'"
        with database.DBConnection(server_paths.SERVER_DB_PATH) as db:
            ret = db.get(sql)
        tables = [table_name for table_name, in ret]
        self.assertTrue("users" in tables)
        self.assertTrue("devices" in tables)
        self.assertTrue("folders" in tables)

