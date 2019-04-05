"""
:module:
:synopsis:
:author: Julian Sobott

"""
import datetime
import unittest
import uuid
import secrets

from server_side import database, paths
from general.database import delete_db_file
from src.tests.server_side.database import test_users
from src.tests.od_logging import logger


class TestDatabaseDevices(unittest.TestCase):

    def setUp(self):
        delete_db_file(paths.SERVER_DB_PATH)
        database.create_database()
        self._dummy_user = test_users.TestDatabaseUsers.helper_create_dummy_user()

    @staticmethod
    def helper_create_dummy_folder():
        pass

    def test_columns(self):
        with database.DBConnection(paths.SERVER_DB_PATH) as db:
            res = db.get("PRAGMA table_info(folders)")
            table_names = [col[1] for col in res]
            expected = ["folder_id", "user_id", "folder_name"]
            self.assertEqual(table_names, expected, "Column names changes")

    def test_create_non_existing(self):
        folder_name = "Dummy_folder"
        folder_id = database.Folder.create(self._dummy_user.user_id, folder_name)
        folder = database.Folder.from_id(folder_id)
        self.assertEqual(folder.folder_name, folder_name)
        self.assertEqual(folder.user_id, self._dummy_user.user_id)
