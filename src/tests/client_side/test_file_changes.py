import unittest
import os
import shutil
from thread_testing import wait_till_condition

from client_side import database, paths, file_watcher
from general.database import delete_db_file
from src.tests.od_logging import logger


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


class TestFileCreate(TestFileChange):

    def create_file(self, ignore=False, folder_id=None, is_folder=False):
        file_watcher.start_observing()
        ignore_patterns = []
        if ignore:
            ignore_patterns = [".*\\.txt"]
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

    def test_create_folder(self):
        self.create_file(is_folder=True)

    def test_create_many(self):
        file_watcher.start_observing()
        ignore_patterns = [".*\\.pyc", ".*\\\\ignore\\\\.+"]
        file_watcher.add_watcher(self.abs_folder_path, ignore_patterns=ignore_patterns, folder_id=self.folder_id)
        # root: 10 files + 1 folder
        for i in range(10):
            rel_file_path = f"file_{i}.txt"
            abs_file_path = os.path.join(self.abs_folder_path, rel_file_path)
            with open(abs_file_path, "w"):
                pass
        rel_folder_path = "folder_1"
        folder_1_path = os.path.join(self.abs_folder_path, rel_folder_path)
        os.mkdir(folder_1_path)

        # folder_1: 1 ignore folder + 1 ignore_file.pyc + 1 not_ignore.txt
        rel_folder_path = "ignore"
        ignore_folder_path = os.path.join(folder_1_path, rel_folder_path)
        os.mkdir(ignore_folder_path)

        abs_file_path = os.path.join(folder_1_path, "ignore_file.pyc")
        with open(abs_file_path, "w"):
            pass

        abs_file_path = os.path.join(folder_1_path, "not_ignore_file.txt")
        with open(abs_file_path, "w"):
            pass
        # ignore folder: 1 file1.txt

        abs_file_path = os.path.join(ignore_folder_path, "file_1.txt")
        with open(abs_file_path, "w"):
            pass
        wait_till_condition(lambda: database.Change.get_possible_entry(self.folder_id, "folder_1/not_ignore_file.txt") is not None)
        changes = database.Change.get_all_folder_entries(self.folder_id)
        num_files = 0
        num_folders = 0
        for change in changes:
            num_folders += change.is_folder
            num_files += not change.is_folder
        self.assertEqual(11, num_files)
        self.assertEqual(2, num_folders)


class TestEditFile(TestFileChange):

    def setUp(self):
        super().setUp()
        self.rel_file_path = "test.txt"
        self.abs_file_path = os.path.join(self.abs_folder_path, self.rel_file_path)
        with open(self.abs_file_path, "w"):
            pass

    def test_edit_file(self):
        file_watcher.start_observing()
        file_watcher.add_watcher(self.abs_folder_path, folder_id=self.folder_id)
        with open(self.abs_file_path, "w") as f:
            f.write(100*"Edited text")
        found_possible = wait_till_condition(
            lambda: database.Change.get_possible_entry(self.folder_id, self.rel_file_path) is not None,
            interval=0.5, timeout=1)
        change = database.Change.get_possible_entry(self.folder_id, self.rel_file_path)
        self.assertIsInstance(change, database.Change)
        is_folder = False
        expected_change = database.Change(1, self.folder_id, self.rel_file_path, is_folder=is_folder,
                                          last_change_time_stamp=change.last_change_time_stamp,
                                          is_created=False, is_moved=False, is_deleted=False, is_modified=True,
                                          necessary_action=database.Change.ACTION_PULL)
        self.assertEqual(expected_change, change)


if __name__ == '__main__':
    unittest.main()
