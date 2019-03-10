import unittest
import os

from client_side import database, paths
from datetime import datetime
from context import logger


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
        self.assertTrue("sync_folders" in tables)
        self.assertTrue("ignores" in tables)
        self.assertTrue("changes" in tables)

    def test_create_database_existing(self):
        delete_database()
        database.create_database()
        self.assertRaises(FileExistsError, database.create_database)


class TestEmptyAccess(unittest.TestCase):
    """Access to the empty db"""

    def setUp(self):
        delete_database()
        database.create_database()

    def test_change_create(self):
        change_id = database.Change.create(1, 'test.txt', is_created=True)
        self.assertEqual(1, change_id)

    def test_change_getter(self):
        folder_id = 1
        rel_path = 'v/test.txt'
        is_created = True
        change_id = database.Change.create(folder_id, rel_path, is_created=is_created)
        change = database.Change(change_id)
        self.assertEqual(folder_id, change.folder_id)
        self.assertEqual(rel_path, change.current_rel_path)
        self.assertEqual(is_created, change.is_created)

    def test_change_setter(self):
        change_id = database.Change.create(1, 'test.txt', is_created=True)
        change = database.Change(change_id)
        change.is_deleted = 1
        new_change = database.Change(change_id)
        self.assertEqual(True, new_change.is_deleted)

    def test_ignores_setter(self):
        ignore_id = database.Ignore.create(1, "folder1/*")
        ignore = database.Ignore(ignore_id)
        ignore.pattern = "new_pattern/*"
        new_ignore = database.Ignore(ignore_id)
        self.assertEqual("new_pattern/*", new_ignore.pattern)

    def test_sync_folders(self):
        folder_id = database.SyncFolder.create("C:/folder1/")
        folder = database.SyncFolder(folder_id)
        folder.abs_path = "C:/new_path/folder_1/"
        new_folder = folder.update()
        self.assertEqual("C:/new_path/folder_1/", new_folder.abs_path)
        self.assertEqual("C:/new_path/folder_1/", folder.abs_path)


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
