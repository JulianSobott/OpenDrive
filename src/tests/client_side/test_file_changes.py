import time
import unittest
import os
import shutil
from thread_testing import wait_till_condition

from OpenDrive.client_side import database, paths, file_changes, file_changes_json
from OpenDrive.general import file_changes_json as gen_json
from tests.helper_all import h_clear_init_all_folders, h_create_empty
from tests.client_side.helper_client import h_get_dummy_folder_data
from src.tests.od_logging import logger


def h_create_empty_dummy_folder(id_: int = 1) -> paths.NormalizedPath:
    path = os.path.join(paths.LOCAL_CLIENT_DATA, f"dummy_folder_{id_}")
    h_create_empty(path)
    return paths.normalize_path(path)


def h_create_expected_change(rel_file_path: str, action: gen_json.ActionType, is_folder: bool = False,
                             new_file_path: str = None):
    dummy_changes = {}
    file_changes_json.gen_json._add_new_change_entry(dummy_changes, paths.normalize_path(rel_file_path), action,
                                                     is_folder, new_file_path)

    actual_path = rel_file_path if new_file_path is None else new_file_path
    expected_change = dummy_changes[actual_path]
    if new_file_path:
        expected_change["new_file_path"] = new_file_path
    return expected_change


def h_min_equal_changes(test_object: unittest.TestCase, expected_change, folder_path, expected_min_changes=1,
                        second_expected_change=None):
    folder = file_changes_json.get_folder_entry(folder_path)
    test_object.assertGreaterEqual(expected_min_changes, len(folder["changes"]))
    if expected_min_changes == 0:
        test_object.assertEqual(0, len(folder["changes"]))
        return
    change = folder["changes"][expected_change["new_file_path"]]
    expected_change["last_change_time_stamp"] = change["last_change_time_stamp"]
    test_object.assertEqual(expected_change, change)
    if second_expected_change:
        second_change = folder["changes"][second_expected_change["new_file_path"]]
        expected_change["last_change_time_stamp"] = second_change["last_change_time_stamp"]
        test_object.assertEqual(expected_change, change)


class TestFileChange(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        h_clear_init_all_folders()

    def setUp(self):
        file_changes_json.init_file()
        self.abs_folder_path = h_create_empty_dummy_folder()
        file_changes.start_observing()

    def tearDown(self):
        file_changes.stop_observing()
        shutil.rmtree(self.abs_folder_path, ignore_errors=True)


class TestFileCreate(TestFileChange):

    def create_file(self, ignore=False, is_folder=False):
        ignore_patterns = []
        if ignore:
            ignore_patterns = [".*\\.txt"]
        file_changes.add_folder(self.abs_folder_path, exclude_regexes=ignore_patterns)
        if is_folder:
            rel_file_path = "dummy"
            os.mkdir(os.path.join(self.abs_folder_path, rel_file_path))
        else:
            rel_file_path = "test.txt"
            abs_file_path = os.path.join(self.abs_folder_path, rel_file_path)
            with open(abs_file_path, "w") as f:
                f.write("Hello" * 10)
        time.sleep(1)
        expected_change = h_create_expected_change(rel_file_path, gen_json.ACTION_PULL, is_folder)
        h_min_equal_changes(self, expected_change, self.abs_folder_path, 0 if ignore else 1)

    def test_create_file(self):
        """no folder_id, no ignore_patterns"""
        self.create_file()

    def test_create_folder(self):
        self.create_file(is_folder=True)

    def test_create_file_not_included(self):
        self.create_file(ignore=True)

    def test_create_many(self):
        ignore_patterns = [".*\\.pyc", ".*\\\\ignore\\\\.+"]
        file_changes.add_folder(self.abs_folder_path, exclude_regexes=ignore_patterns)
        # root: 10 files + 1 folder
        for i in range(10):
            rel_file_path = f"file_{i}.txt"
            abs_file_path = os.path.join(self.abs_folder_path, rel_file_path)
            with open(abs_file_path, "w") as f:
                f.write("HeHe" * 10)
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
        time.sleep(2)
        folder = file_changes_json.get_folder_entry(self.abs_folder_path)
        changes = folder["changes"]
        num_files = 0
        num_folders = 0
        for change in changes.values():
            num_folders += change["is_directory"]
            num_files += not change["is_directory"]
        self.assertEqual(11, num_files)
        self.assertEqual(2, num_folders)


class TestFileChanges(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        h_clear_init_all_folders()

    def setUp(self):
        file_changes_json.init_file()
        self.abs_folder_path = h_create_empty_dummy_folder()
        self.rel_file_path = "test.txt"
        self.abs_file_path = os.path.join(self.abs_folder_path, self.rel_file_path)
        with open(self.abs_file_path, "w"):
            pass
        file_changes.start_observing()
        file_changes.add_folder(self.abs_folder_path)

    def tearDown(self):
        file_changes.stop_observing()
        shutil.rmtree(self.abs_folder_path, ignore_errors=True)

    def test_edit_file(self):
        with open(self.abs_file_path, "w") as f:
            f.write(100 * "Edited text")
        time.sleep(0.5)
        expected_change = h_create_expected_change(self.rel_file_path, gen_json.ACTION_PULL)
        h_min_equal_changes(self, expected_change, self.abs_folder_path)

    def test_create_edit_file(self):
        rel_file_path = "test2.txt"
        with open(os.path.join(self.abs_folder_path, rel_file_path), "w") as f:
            f.write(100 * "Edited text")
        time.sleep(0.5)
        expected_change = h_create_expected_change(rel_file_path, gen_json.ACTION_PULL)
        h_min_equal_changes(self, expected_change, self.abs_folder_path)

    def test_remove_file(self):
        os.remove(self.abs_file_path)
        time.sleep(0.5)
        expected_change = h_create_expected_change(self.rel_file_path, gen_json.ACTION_DELETE)
        h_min_equal_changes(self, expected_change, self.abs_folder_path)

    def test_move_same_folder(self):
        new_rel_path = "test2.txt"
        shutil.move(self.abs_file_path, os.path.join(self.abs_folder_path, new_rel_path))
        time.sleep(0.5)
        expected_change = h_create_expected_change(self.rel_file_path, gen_json.ACTION_MOVE, new_file_path=new_rel_path)
        h_min_equal_changes(self, expected_change, self.abs_folder_path)

    def test_twice_move(self):
        new_rel_path = "test2.txt"
        new_abs_path = os.path.join(self.abs_folder_path, new_rel_path)
        shutil.move(self.abs_file_path, new_abs_path)
        new_rel_path = "test3.txt"
        shutil.move(new_abs_path, os.path.join(self.abs_folder_path, new_rel_path))
        time.sleep(1)
        expected_change = h_create_expected_change(self.rel_file_path, gen_json.ACTION_MOVE, new_file_path=new_rel_path)
        h_min_equal_changes(self, expected_change, self.abs_folder_path)

    def test_move_modify(self):
        new_rel_path = "test2.txt"
        new_abs_path = os.path.join(self.abs_folder_path, new_rel_path)
        shutil.move(self.abs_file_path, new_abs_path)
        with open(new_abs_path, "w") as f:
            f.write("Modified")
        time.sleep(0.5)
        expected_change_delete = h_create_expected_change(self.rel_file_path, gen_json.ACTION_DELETE)
        expected_change_pull = h_create_expected_change(new_rel_path, gen_json.ACTION_PULL)
        h_min_equal_changes(self, expected_change_delete, self.abs_folder_path, 2, expected_change_pull)


class TestAPI(unittest.TestCase):

    def setUp(self):
        file_changes_json.init_file()

    def tearDown(self):
        file_changes.stop_observing()

    def test_start_observing(self):
        file_changes_json.init_file()
        path, include, exclude = h_get_dummy_folder_data()
        file_changes.add_folder(path, include, exclude)
        file_changes.start_observing()
        self.assertEqual(1, len(file_changes.watchers))

    def test_add_single_ignores(self):
        folder_path = h_create_empty_dummy_folder()
        file_changes.start_observing()
        file_changes.add_folder(folder_path)
        rel_path = paths.normalize_path("test.txt")
        file_changes.add_single_ignores(folder_path, [rel_path])
        with open(os.path.join(folder_path, rel_path), "w+") as f:
            f.write("Hello" * 100)

        folder = file_changes_json.get_folder_entry(folder_path)
        self.assertEqual(0, len(folder["changes"]))

    def test_remove_single_ignores(self):
        folder_path = h_create_empty_dummy_folder()
        file_changes.start_observing()
        file_changes.add_folder(folder_path)
        rel_path = paths.normalize_path("test.txt")
        file_changes.add_single_ignores(folder_path, [rel_path])
        file_changes.remove_single_ignore(folder_path, rel_path)
        with open(os.path.join(folder_path, rel_path), "w+") as f:
            f.write("Hello" * 100)

        folder = file_changes_json.get_folder_entry(folder_path)
        self.assertEqual(1, len(folder["changes"]))

    def test_add_folder(self):
        file_changes_json.init_file()
        path, include, exclude = h_get_dummy_folder_data()
        file_changes.add_folder(path, include, exclude)
        self.assertEqual(1, len(file_changes.watchers))
        self.assertEqual([path], gen_json.get_all_synced_folders_paths())

    def test_remove_folder(self):
        file_changes.start_observing()
        path, _, _ = h_get_dummy_folder_data()
        file_changes.add_folder(path)
        file_changes.remove_folder_from_watching(path)
        self.assertEqual(0, len(file_changes.watchers))


if __name__ == '__main__':
    unittest.main()
