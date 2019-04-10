"""
:module:
:synopsis:
:author: Julian Sobott
"""
import unittest

from OpenDrive.server_side import database, paths
from OpenDrive.general.database import delete_db_file
from tests.od_logging import logger


class TestDatabaseUsers(unittest.TestCase):

    def setUp(self):
        delete_db_file(paths.SERVER_DB_PATH)
        database.create_database()

    @staticmethod
    def helper_create_dummy_user():
        username = "Tom"
        password = "asj&kdkl$asjd345a!d:-"
        email = "Tom@gmail.com"
        user_id = database.User.create(username, password, email)
        return database.User(user_id, username, password, email)

    def test_columns(self):
        with database.DBConnection(paths.SERVER_DB_PATH) as db:
            res = db.get("PRAGMA table_info(users)")
            table_names = [col[1] for col in res]
            expected = ["user_id", "username", "password", "email"]
            self.assertEqual(table_names, expected, "Column names changes")

    def test_create_non_existing(self):
        username = "Tom"
        password = "asj&kdkl$asjd345a!d:-"
        user_id = database.User.create(username, password)
        user = database.User.from_id(user_id)
        self.assertEqual(user.username, username)
        self.assertEqual(user.password, password)
        self.assertEqual(user.email, None)

    def test_get_by_username(self):
        expected = self.helper_create_dummy_user()
        user = database.User.get_by_username("Tom")
        self.assertEqual(expected, user)
        user_2 = database.User.get_by_username("tom")
        self.assertEqual(None, user_2)
