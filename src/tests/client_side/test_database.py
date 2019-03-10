import unittest
import os

from client_side import database, paths
from datetime import datetime


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
        with database.DBConnection(paths.LOCAL_DB_PATH) as db:
            ret = db.get(sql)
        tables = [table_name for table_name, in ret]
        print(tables)
        self.assertEqual(len(tables), 3)
        self.assertTrue("sync_folders" in tables)
        self.assertTrue("ignores" in tables)
        self.assertTrue("changes" in tables)

    def test_create_database_existing(self):
        delete_database()
        database.create_database()
        self.assertRaises(FileExistsError, database.create_database)


class TestAccess(unittest.TestCase):

    def setUp(self):
        delete_database()
        database.create_database()
        sql_folder_insert = "INSERT INTO 'sync_folders' ('abs_path') VALUES (?)"
        with database.DBConnection(paths.LOCAL_DB_PATH) as db:
            folder_id = db.insert(sql_folder_insert, ('C:/folder1/',))
        database.Change.create(folder_id, 'test.txt', is_created=True)

    def tearDown(self):
        pass

    def test_get_existing_change_entry(self):
        pass
        # , folder_id, rel_path


if __name__ == '__main__':
    unittest.main()
