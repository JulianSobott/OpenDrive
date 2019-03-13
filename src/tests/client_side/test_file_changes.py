import unittest
import os
import shutil
from thread_testing import wait_till_condition

from client_side import database, paths, file_watcher
from general.database import delete_db_file
from src.tests.Logging import logger


class TestFileChange(unittest.TestCase):
    abs_folder_path = os.path.join(paths.PROJECT_PATH, "local/client_side/dummy_folder/")
    folder_id: int

    def setUp(self):
        delete_db_file(paths.LOCAL_DB_PATH)
        database.create_database()
        try:
            os.mkdir(self.abs_folder_path)
        except FileExistsError:
            shutil.rmtree(self.abs_folder_path, ignore_errors=True)
            os.mkdir(self.abs_folder_path)
        self.folder_id = database.SyncFolder.create(self.abs_folder_path)

    def tearDown(self):
        file_watcher.stop_observing()
        shutil.rmtree(self.abs_folder_path, ignore_errors=True)

    def create_file(self, ignore=False, folder_id=None, is_folder=False):
        file_watcher.start_observing()
        ignore_patterns = []
        if ignore:
            ignore_patterns = ["*.txt"]
        file_watcher.add_watcher(self.abs_folder_path, ignore_patterns=ignore_patterns, folder_id=folder_id)
        if is_folder:
            rel_file_path = "dummy"
            os.mkdir(os.path.join(self.abs_folder_path, rel_file_path))
        else:
            rel_file_path = "test.txt"
            abs_file_path = os.path.join(self.abs_folder_path, rel_file_path)
            with open(abs_file_path, "w"):
                pass
        found_possible = wait_till_condition(
            lambda: database.Change.get_possible_entry(self.folder_id, rel_file_path) is not None,
            interval=0.5, timeout=1)
        if ignore:
            self.assertEqual(found_possible, False)
        else:
            change = database.Change.get_possible_entry(self.folder_id, rel_file_path)
            self.assertIsInstance(change, database.Change)
            expected_change = database.Change(1, self.folder_id, rel_file_path, is_folder=is_folder,
                                              last_change_time_stamp=change.last_change_time_stamp, is_created=True,
                                              is_moved=False,
                                              is_deleted=False, is_modified=False,
                                              necessary_action=database.Change.ACTION_PULL)
            self.assertEqual(expected_change, change)

    def test_create_file(self):
        """no folder_id, no ignore_patterns"""
        self.create_file()

    def test_create_file_folder_id(self):
        """folder_id, no ignore_patterns"""
        self.create_file(folder_id=self.folder_id)

    def test_create_file_ignored(self):
        """no folder_id, ignore_patterns"""
        self.create_file(ignore=True)


if __name__ == '__main__':
    unittest.main()
