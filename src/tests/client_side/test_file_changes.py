import os
import shutil
import time
import unittest
from unittest.mock import *
from pynetworking import client, server

from OpenDrive.client_side import paths, file_changes, file_changes_json
from OpenDrive.client_side.gui.explorer import pattern_parser
from OpenDrive.general import file_changes_json as gen_json
from tests.client_side.helper_client import h_get_dummy_folder_data
from tests.helper_all import h_clear_init_all_folders, h_create_empty, MockFile


class TestFileChange(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        h_clear_init_all_folders()

    def setUp(self):
        file_changes_json.init_file(empty=True)
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
        file_changes.add_folder(self.abs_folder_path, "server/path", exclude_regexes=ignore_patterns)
        if is_folder:
            rel_file_path = "dummy"
            os.mkdir(os.path.join(self.abs_folder_path, rel_file_path))
        else:
            rel_file_path = "test.txt"
            abs_file_path = os.path.join(self.abs_folder_path, rel_file_path)
            with open(abs_file_path, "w") as f:
                f.write("Hello" * 10)
        time.sleep(1)
        expected_changes = {}
        if is_folder:
            action = gen_json.ACTION_MKDIR
        else:
            action = gen_json.ACTION_PULL
        gen_json._add_new_change_entry(expected_changes, paths.normalize_path(rel_file_path), action, is_folder)
        data = gen_json._get_json_data()
        actual_changes = data[self.abs_folder_path]["changes"]
        if ignore:
            self.assertEqual({}, actual_changes)
        else:
            expected_changes[rel_file_path]["timestamp"] = actual_changes[rel_file_path]["timestamp"]
            self.assertEqual(expected_changes, actual_changes)

    def test_create_file(self):
        """no folder_id, no ignore_patterns"""
        self.create_file()

    def test_create_folder(self):
        self.create_file(is_folder=True)

    def test_create_file_not_included(self):
        self.create_file(ignore=True)

    def test_create_many(self):
        ignore_patterns = pattern_parser.parse_patterns("*.pyc, *ignore*")
        file_changes.add_folder(self.abs_folder_path, "server/path", exclude_regexes=ignore_patterns)
        time.sleep(0.5)
        # root: 10 files + 1 folder
        for i in range(10):
            rel_file_path = f"file_{i}.txt"
            abs_file_path = os.path.join(self.abs_folder_path, rel_file_path)
            with open(abs_file_path, "w") as f:
                f.write("HeHe" * 10)
            time.sleep(0.1)
        rel_folder_path = "folder_1"
        folder_1_path = os.path.join(self.abs_folder_path, rel_folder_path)
        os.mkdir(folder_1_path)

        # folder_1: 1 ignore folder + 1 ignore_file.pyc + 1 not_ignore.txt
        rel_folder_path = "ignore"
        ignore_folder_path = os.path.join(folder_1_path, rel_folder_path)
        os.mkdir(ignore_folder_path)

        abs_file_path = os.path.join(folder_1_path, "file.pyc")
        with open(abs_file_path, "w"):
            pass

        abs_file_path = os.path.join(folder_1_path, "not_Iggnore_file.txt")
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
        self.assertEqual(1, num_folders)


class TestFileChanges(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        h_clear_init_all_folders()

    def setUp(self):
        file_changes_json.init_file(empty=True)
        self.abs_folder_path = h_create_empty_dummy_folder()
        self.rel_file_path = "test.txt"
        self.abs_file_path = os.path.join(self.abs_folder_path, self.rel_file_path)
        with open(self.abs_file_path, "w"):
            pass
        file_changes.start_observing()
        file_changes.add_folder(self.abs_folder_path, "server/path")

    def tearDown(self):
        file_changes.stop_observing()
        shutil.rmtree(self.abs_folder_path, ignore_errors=True)

    def test_edit_file(self):
        with open(self.abs_file_path, "w") as f:
            f.write(100 * "Edited text")
        time.sleep(0.5)
        expected_changes = h_create_expected_change(self.rel_file_path, gen_json.ACTION_PULL)
        h_min_equal_changes(self, expected_changes, self.abs_folder_path, self.rel_file_path)

    def test_create_edit_file(self):
        rel_file_path = "test2.txt"
        with open(os.path.join(self.abs_folder_path, rel_file_path), "w") as f:
            f.write(100 * "Edited text")
        time.sleep(0.5)
        expected_change = h_create_expected_change(rel_file_path, gen_json.ACTION_PULL)
        h_min_equal_changes(self, expected_change, self.abs_folder_path, rel_file_path)

    def test_remove_file(self):
        os.remove(self.abs_file_path)
        time.sleep(0.5)
        expected_change = h_create_expected_change(self.rel_file_path, gen_json.ACTION_DELETE)
        h_min_equal_changes(self, expected_change, self.abs_folder_path, self.rel_file_path)

    def test_move_same_folder(self):
        new_rel_path = "test2.txt"
        shutil.move(self.abs_file_path, os.path.join(self.abs_folder_path, new_rel_path))
        time.sleep(0.5)
        expected_change = h_create_expected_change(self.rel_file_path, gen_json.ACTION_MOVE, new_file_path=new_rel_path)
        h_min_equal_changes(self, expected_change, self.abs_folder_path, new_rel_path)

    def test_twice_move(self):
        new_rel_path = "test2.txt"
        new_abs_path = os.path.join(self.abs_folder_path, new_rel_path)
        shutil.move(self.abs_file_path, new_abs_path)
        new_rel_path = "test3.txt"
        shutil.move(new_abs_path, os.path.join(self.abs_folder_path, new_rel_path))
        time.sleep(1)
        expected_change = h_create_expected_change(self.rel_file_path, gen_json.ACTION_MOVE, new_file_path=new_rel_path)
        h_min_equal_changes(self, expected_change, self.abs_folder_path, new_rel_path)

    def test_move_modify(self):
        new_rel_path = "test2.txt"
        new_abs_path = os.path.join(self.abs_folder_path, new_rel_path)
        shutil.move(self.abs_file_path, new_abs_path)
        with open(new_abs_path, "w") as f:
            f.write("Modified")
        time.sleep(0.5)
        expected_change_delete = h_create_expected_change(self.rel_file_path, gen_json.ACTION_DELETE)
        expected_change_pull = h_create_expected_change(new_rel_path, gen_json.ACTION_PULL)
        h_min_equal_changes(self, expected_change_delete, self.abs_folder_path, self.rel_file_path)
        h_min_equal_changes(self, expected_change_pull, self.abs_folder_path, new_rel_path)


class TestAPI(unittest.TestCase):

    def tearDown(self):
        try:
            file_changes.stop_observing()
        except RuntimeError:
            pass

    def test_start_observing_no_folders(self):
        m_init = Mock(return_value=None)
        m_add = Mock()
        with patch("OpenDrive.client_side.file_changes_json.init_file", m_init), \
                patch("OpenDrive.client_side.file_changes_json.get_all_data", return_value={}),\
                patch("OpenDrive.client_side.file_changes._add_watcher", m_add):
            file_changes.start_observing()
            m_init.assert_called_once()
            m_add.assert_not_called()

    def test_start_observing(self):
        m_init = Mock(return_value=None)
        m_add = Mock(retun_value=None)
        all_folders = {"path/to\\folder": {"include_regexes": [".*"], "exclude_regexes": []},
                       "path/to\\folder2": {"include_regexes": [".*"], "exclude_regexes": [".txt"]}}
        with patch("OpenDrive.client_side.file_changes_json.init_file", m_init), \
             patch("OpenDrive.client_side.file_changes_json.get_all_data", return_value=all_folders), \
             patch("OpenDrive.client_side.file_changes._add_watcher", m_add):
            file_changes.start_observing()
            m_init.assert_called_once()
            self.assertEqual(2, m_add.call_count)

    def test_stop_observing_started(self):
        file_changes.observer.start()
        file_changes.stop_observing()

    def test_stop_observing_not_started(self):
        file_changes.stop_observing()

    def test_add_folder_success(self):
        with patch("OpenDrive.client_side.file_changes_json.add_folder", return_value=True), \
                patch("os.path.exists", return_value=True):
            ret = file_changes.add_folder("path/to\\folder", "server/path")
            self.assertTrue(ret)
            self.assertEqual(1, len(file_changes.watchers))

    def test_add_folder_fail(self):
        with patch("OpenDrive.client_side.file_changes_json.add_folder", return_value=False), \
                patch("os.path.exists", return_value=True):
            ret = file_changes.add_folder("path/to\\folder", "server/path")
            self.assertFalse(ret)
            self.assertEqual(0, len(file_changes.watchers))

    def test_add_folder_fail2(self):
        with patch("OpenDrive.client_side.file_changes_json.add_folder", return_value=True), \
                patch("os.path.exists", return_value=False):
            ret = file_changes.add_folder("path/to\\folder", "server/path")
            self.assertFalse(ret)
            self.assertEqual(0, len(file_changes.watchers))

    def test_remove_folder_success(self):
        # no mocking of the json file
        file_changes_json.init_file(empty=True)
        with patch("os.path.exists", return_value=True):
            file_changes.add_folder("existing/folder", "server/path")
            file_changes.remove_folder_from_watching("existing/folder")
            self.assertEqual(0, len(file_changes.watchers))
            self.assertEqual({}, file_changes_json.get_all_data())

    def test_remove_folder_fail(self):
        # no mocking of the json file
        file_changes_json.init_file(empty=True)
        file_changes.remove_folder_from_watching("not_existing/folder")
        self.assertEqual(0, len(file_changes.watchers))
        self.assertEqual({}, file_changes_json.get_all_data())

    def test_add_single_ignores(self):
        pass    # TODO

    def test_remove_single_ignores(self):
        pass  # TODO


def h_create_empty_dummy_folder(id_: int = 1) -> paths.NormalizedPath:
    path = os.path.join(paths.LOCAL_CLIENT_DATA, f"dummy_folder_{id_}")
    h_create_empty(path)
    return paths.normalize_path(path)


def h_create_expected_change(rel_file_path: str, action: gen_json.ActionType, is_folder: bool = False,
                             new_file_path: str = None):
    expected_changes = {}
    gen_json._add_new_change_entry(expected_changes, paths.normalize_path(rel_file_path), action, is_folder,
                                   new_file_path)
    return expected_changes


def h_min_equal_changes(test_object: unittest.TestCase, expected_changes, folder_path, rel_file_path):
    data = gen_json._get_json_data()
    actual_changes = data[folder_path]["changes"]
    expected_changes[rel_file_path]["timestamp"] = actual_changes[rel_file_path]["timestamp"]
    test_object.assertEqual(expected_changes[rel_file_path], actual_changes[rel_file_path])


if __name__ == '__main__':
    unittest.main()
