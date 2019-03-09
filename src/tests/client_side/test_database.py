import unittest
import os

from client_side import database, paths


class TestDatabase(unittest.TestCase):

    def test_create_database_non_existing(self):
        database.create_database()
        self.assertTrue(os.path.exists(paths.LOCAL_DB_PATH),
                        "Database file was not created or created at the wrong place!")

    def test_create_database_existing(self):
        self.assertRaises(FileExistsError, database.create_database,
                          "No error raised, although database already exists!")


if __name__ == '__main__':
    unittest.main()
