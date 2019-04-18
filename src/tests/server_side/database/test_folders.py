"""
:module:
:synopsis:
:author: Julian Sobott

"""
import unittest
from OpenDrive.server_side import database, paths
from tests.server_side.database.helper_database import h_setup_server_database, h_create_dummy_user


class TestDatabaseDevices(unittest.TestCase):

    def setUp(self):
        h_setup_server_database()
        self._dummy_user = h_create_dummy_user()

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
