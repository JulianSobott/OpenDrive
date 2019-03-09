import unittest
import os
import sqlite3

from client_side import database, paths


def delete_database():
    try:
        os.remove(paths.LOCAL_DB_PATH)
    except FileNotFoundError:
        pass


class TestDatabaseConnections(unittest.TestCase):

    def test_create_database_non_existing(self):
        delete_database()
        database.create_database()
        self.assertTrue(os.path.exists(paths.LOCAL_DB_PATH),
                        "Database file was not created or created at the wrong place!")

    def test_tables_creation(self):
        delete_database()
        database.create_database()
        sql = "SELECT name  FROM sqlite_master WHERE type='table'"
        with database.DBConnection() as db:
            ret = db.get(sql)
        tables = [table_name for table_name, in ret]
        self.assertEqual(len(tables), 2)
        self.assertTrue("sync_folders" in tables)

    def test_create_database_existing(self):
        delete_database()
        database.create_database()
        self.assertRaises(FileExistsError, database.create_database)


if __name__ == '__main__':
    unittest.main()
