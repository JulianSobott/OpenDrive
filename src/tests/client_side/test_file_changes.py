import time
import unittest
import os
import shutil
from thread_testing import wait_till_condition

from OpenDrive.client_side import database, paths, file_changes, file_changes_json
from OpenDrive.general.database import delete_db_file
from tests.helper_all import h_clear_init_all_folders
from tests.client_side.helper_client import h_get_dummy_folder_data
from src.tests.od_logging import logger


class TestFileChange(unittest.TestCase):
    abs_folder_path = os.path.join(paths.LOCAL_CLIENT_DATA, "dummy_folder/")
    folder_id: int

    @classmethod
    def setUpClass(cls) -> None:
        h_clear_init_all_folders()

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
        file_changes.stop_observing()
        shutil.rmtree(self.abs_folder_path, ignore_errors=True)


class TestFileCreate(TestFileChange):

    def create_file(self, ignore=False, is_folder=False):
        file_changes.start_observing()
        ignore_patterns = []
        if ignore:
            ignore_patterns = [".*\\.txt"]
        file_changes.add_watcher(self.abs_folder_path, exclude_regexes=ignore_patterns)
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
            expected_change = database.Change(change.id, self.folder_id, rel_file_path, is_folder=is_folder,
                                              last_change_time_stamp=change.last_change_time_stamp, is_created=True,
                                              is_moved=False,
                                              is_deleted=False, is_modified=False,
                                              necessary_action=database.Change.ACTION_PULL)
            self.assertEqual(expected_change, change)

    def test_create_file(self):
        """no folder_id, no ignore_patterns"""
        self.create_file()

    def test_create_file_ignored(self):
        """no folder_id, ignore_patterns"""
        self.create_file(ignore=True)

    def test_create_folder(self):
        self.create_file(is_folder=True)

    def test_create_file_not_included(self):
        file_changes.start_observing()
        file_changes.add_watcher(self.abs_folder_path, include_regexes=[".*\\.txt"], )
        with open(os.path.join(self.abs_folder_path, "dummy.py"), "w+") as f:
            pass
        wait_till_condition(lambda: True is False, timeout=0.5)
        self.assertIsNone(database.Change.get_possible_entry(self.folder_id, "dummy.py"))

    def test_create_many(self):
        file_changes.start_observing()
        ignore_patterns = [".*\\.pyc", ".*\\\\ignore\\\\.+"]
        file_changes.add_watcher(self.abs_folder_path, exclude_regexes=ignore_patterns, folder_id=self.folder_id)
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
        file_changes.start_observing()
        file_changes.add_watcher(self.abs_folder_path, folder_id=self.folder_id)

    def test_edit_file(self):
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

    def test_create_edit_file(self):
        rel_file_path = "test2.txt"
        with open(os.path.join(self.abs_folder_path, rel_file_path), "w") as f:
            f.write(100*"Edited text")
        wait_till_condition(lambda: False, timeout=0.5)     # Ensures, both data is in DB
        wait_till_condition(
            lambda: database.Change.get_possible_entry(self.folder_id, rel_file_path) is not None,
            interval=0.5, timeout=1)
        change = database.Change.get_possible_entry(self.folder_id, rel_file_path)
        self.assertIsInstance(change, database.Change)
        is_folder = False
        expected_change = database.Change(1, self.folder_id, rel_file_path, is_folder=is_folder,
                                          last_change_time_stamp=change.last_change_time_stamp,
                                          is_created=True, is_moved=False, is_deleted=False, is_modified=True,
                                          necessary_action=database.Change.ACTION_PULL)
        self.assertEqual(expected_change, change)


class TestRemove(TestFileChange):

    def setUp(self):
        super().setUp()
        self.rel_file_path = "test.txt"
        self.abs_file_path = os.path.join(self.abs_folder_path, self.rel_file_path)
        with open(self.abs_file_path, "w"):
            pass
        file_changes.start_observing()
        file_changes.add_watcher(self.abs_folder_path, folder_id=self.folder_id)

    def test_remove_file(self):
        os.remove(self.abs_file_path)
        wait_till_condition(
            lambda: database.Change.get_possible_entry(self.folder_id, self.rel_file_path) is not None,
            interval=0.1, timeout=1)
        change = database.Change.get_possible_entry(self.folder_id, self.rel_file_path)
        self.assertIsInstance(change, database.Change)
        is_folder = False
        expected_change = database.Change(change.id, self.folder_id, self.rel_file_path, is_folder=is_folder,
                                          last_change_time_stamp=change.last_change_time_stamp,
                                          is_created=False, is_moved=False, is_deleted=True, is_modified=False,
                                          necessary_action=database.Change.ACTION_DELETE)
        self.assertEqual(expected_change, change)


class TestMove(TestFileChange):

    def setUp(self):
        super().setUp()
        self.folder_1_path = os.path.join(self.abs_folder_path, "folder_1")
        self.folder_1_id = database.SyncFolder.create(self.folder_1_path)
        os.mkdir(self.folder_1_path)
        self.folder_2_path = os.path.join(self.abs_folder_path, "folder_2")
        self.folder_2_id = database.SyncFolder.create(self.folder_2_path)
        os.mkdir(self.folder_2_path)
        self.rel_test_file_path = "test_file.txt"
        self.test_file_path = os.path.join(self.folder_1_path, self.rel_test_file_path)
        with open(self.test_file_path, "w"):
            pass
        file_changes.start_observing()
        file_changes.add_watcher(self.folder_1_path, folder_id=self.folder_1_id)
        file_changes.add_watcher(self.folder_2_path, folder_id=self.folder_2_id)

    def test_move_same_folder(self):
        new_rel_path = "test2.txt"
        shutil.move(self.test_file_path, os.path.join(self.folder_1_path, new_rel_path))
        wait_till_condition(
            lambda: database.Change.get_possible_entry(self.folder_1_id, new_rel_path) is not None,
            interval=0.1, timeout=1)
        change = database.Change.get_possible_entry(self.folder_1_id, new_rel_path)
        self.assertIsInstance(change, database.Change)
        expected_change = database.Change(1, self.folder_1_id, new_rel_path, is_folder=False,
                                          last_change_time_stamp=change.last_change_time_stamp,
                                          is_created=False, is_moved=True, is_deleted=False, is_modified=False,
                                          necessary_action=database.Change.ACTION_MOVE,
                                          old_abs_path=self.test_file_path)
        self.assertEqual(expected_change, change)


class TestAPI(unittest.TestCase):
    abs_folder_path_1 = os.path.join(paths.PROJECT_PATH, "local/client_side/dummy_folder_1/")
    abs_folder_path_2 = os.path.join(paths.PROJECT_PATH, "local/client_side/dummy_folder_2/")

    def setUp(self):
        file_changes_json.init_file()
        try:
            os.mkdir(self.abs_folder_path_1)
        except FileExistsError:
            shutil.rmtree(self.abs_folder_path_1, ignore_errors=True)
            os.mkdir(self.abs_folder_path_1)
        try:
            os.mkdir(self.abs_folder_path_2)
        except FileExistsError:
            shutil.rmtree(self.abs_folder_path_2, ignore_errors=True)
            os.mkdir(self.abs_folder_path_2)
        file_changes.add_folder(self.abs_folder_path_1)
        file_changes.add_folder(self.abs_folder_path_2)

    def tearDown(self):
        file_changes.stop_observing()
        shutil.rmtree(self.abs_folder_path_1, ignore_errors=True)
        shutil.rmtree(self.abs_folder_path_2, ignore_errors=True)

    def test_start(self):
        file_changes_json.init_file()
        path, include, exclude = h_get_dummy_folder_data()
        file_changes.add_folder(path, include, exclude)
        file_changes.start()
        self.assertEqual(1, len(file_changes.watchers))

    def test_add_single_ignores(self):
        rel_file_path = "test.txt"
        abs_file_path = os.path.join(self.abs_folder_path_2, rel_file_path)
        with open(abs_file_path, "w") as f:
            f.write("Hello World" * 100)
        file_changes.start()
        file_changes.add_single_ignores(self.folder_id_1, [rel_file_path])
        time.sleep(1)
        shutil.copy(abs_file_path, self.abs_folder_path_1)
        self.assertEqual(0, len(database.Change.get_all()))

    def test_add_folder(self):
        file_changes_json.init_file()
        path, include, exclude = h_get_dummy_folder_data()
        file_changes.add_folder(path, include, exclude)
        self.assertEqual(1, len(file_changes.watchers))
        self.assertEqual([path], file_changes_json.get_all_synced_folders_paths())

    def test_remove_folder(self):
        file_changes.start()
        file_changes.remove_folder_from_watching(self.abs_folder_path_1)
        self.assertEqual(1, len(file_changes.watchers))

    def test_add_permanent_ignores(self):
        num_ignores = 100
        ignores = [str(i) for i in range(num_ignores)]
        file_changes.add_permanent_ignores(ignores, folder_id=self.folder_id_1)
        self.assertEqual(num_ignores, len(database.Ignore.get_all()))

    def test_remove_permanent_ignores(self):
        num_ignores = 3
        ignores = [str(i) for i in range(num_ignores)]
        file_changes.add_permanent_ignores(ignores, folder_id=self.folder_id_1)
        self.assertEqual(num_ignores, len(database.Ignore.get_all()))
        file_changes.remove_permanent_ignores(ignores, folder_id=self.folder_id_1)
        self.assertEqual(0, len(database.Ignore.get_all()))


if __name__ == '__main__':
    unittest.main()
