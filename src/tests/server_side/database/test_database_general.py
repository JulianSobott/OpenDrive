"""
:module:
:synopsis:
:author: Julian Sobott

"""
import unittest
import os

from server_side import database, paths
from general.database import delete_db_file
from general.paths import normalize_path
from datetime import datetime
from src.tests.od_logging import logger


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

