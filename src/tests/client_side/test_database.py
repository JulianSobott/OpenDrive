import unittest
import os
from typing import List

from client_side import database, paths
from general.database import delete_db_file
from general.paths import normalize_path
from datetime import datetime
from src.tests.od_logging import logger


class TestDatabaseConnections(unittest.TestCase):

    def test_create_database_non_existing(self):
        delete_db_file(paths.LOCAL_DB_PATH)
        database.create_database()
        self.assertTrue(os.path.exists(paths.LOCAL_DB_PATH),
                        "Database file was not created or created at the wrong place!")

    def test_tables_creation(self):
        delete_db_file(paths.LOCAL_DB_PATH)
        database.create_database()
        sql = "SELECT name  FROM sqlite_master WHERE type='table'"
        with database.DBConnection(paths.LOCAL_DB_PATH) as db:
            ret = db.get(sql)
        tables = [table_name for table_name, in ret]
        self.assertTrue("sync_folders" in tables)
        self.assertTrue("ignores" in tables)
        self.assertTrue("changes" in tables)

    def test_create_database_existing(self):
        delete_db_file(paths.LOCAL_DB_PATH)
        database.create_database()
        self.assertRaises(FileExistsError, database.create_database)


class TestEmptyAccess(unittest.TestCase):
    """Access to the empty db"""

    def setUp(self):
        delete_db_file(paths.LOCAL_DB_PATH)
        database.create_database()

    def test_change_create(self):
        change_id = database.Change.create(1, 'test.txt', is_created=True)
        self.assertEqual(1, change_id)

    def test_change_getter(self):
        folder_id = 1
        rel_path = 'v/test.txt'
        is_created = True
        change_id = database.Change.create(folder_id, rel_path, is_created=is_created)
        change = database.Change.from_id(change_id)
        self.assertEqual(folder_id, change.folder_id)
        self.assertEqual(rel_path, change.current_rel_path)
        self.assertEqual(is_created, change.is_created)

    def test_change_setter(self):
        change_id = database.Change.create(1, 'test.txt', is_created=True)
        change = database.Change.from_id(change_id)
        change.is_deleted = 1
        change.update()
        self.assertEqual(True, change.is_deleted)

    def test_ignores_setter(self):
        ignore_id = database.Ignore.create(1, "folder1/*")
        ignore = database.Ignore.from_id(ignore_id)
        ignore.pattern = "new_pattern/*"
        ignore.update()
        self.assertEqual("new_pattern/*", ignore.pattern)

    def test_sync_folders(self):
        folder_id = database.SyncFolder.create("C:/folder1/")
        folder = database.SyncFolder.from_id(folder_id)
        folder.abs_path = "C:/new_path/folder_1/"
        folder.update()
        self.assertEqual(normalize_path("C:/new_path/folder_1/"), folder.abs_path)


class TestAccess(unittest.TestCase):

    def setUp(self):
        delete_db_file(paths.LOCAL_DB_PATH)
        database.create_database()
        folder_id = database.SyncFolder.create('C:/folder1/')
        database.Change.create(folder_id, 'test.txt', is_created=True)

    def tearDown(self):
        pass

    def test_get_existing_change_entry(self):
        folder_id = 1
        rel_path = "test.txt"
        change = database.Change.get_possible_entry(folder_id, rel_path)
        self.assertEqual(rel_path, change.current_rel_path)

    def test_get_non_existing_change_entry(self):
        folder_id = 1
        rel_path = "non_existing.txt"
        change = database.Change.get_possible_entry(folder_id, rel_path)
        self.assertEqual(None, change)


if __name__ == '__main__':
    unittest.main()
