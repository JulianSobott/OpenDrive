import json
import unittest
from pynetworking import client, server

from OpenDrive.client_side import file_changes_json
from OpenDrive.client_side import paths as client_paths
from OpenDrive.general import file_changes_json as gen_json
from tests.client_side.helper_client import h_get_dummy_folder_data


class TestJson(unittest.TestCase):

    def setUp(self) -> None:
        file_changes_json.init_file(empty=True)

    def test_init_file(self):
        file_changes_json.init_file()
        with open(client_paths.LOCAL_JSON_PATH, "r") as file:
            data = json.load(file)
            self.assertEqual({}, data)

    def test_add_folder(self):
        path, include, exclude = h_get_dummy_folder_data()
        server_path = file_changes_json.NormalizedPath("folder_at_server")
        file_changes_json.add_folder(path, include, exclude, server_path)
        data = file_changes_json._get_json_data()
        expected = {path: {"server_folder_path": server_path, "include_regexes": include, "exclude_regexes": exclude,
                           "changes": {}}}
        self.assertEqual(expected, data)

    def test_add_folder_existing(self):
        file_changes_json.init_file()
        path, include, exclude = h_get_dummy_folder_data()
        added = file_changes_json.add_folder(path, include, exclude, client_paths.normalize_path("server/path"))
        self.assertTrue(added)
        added = file_changes_json.add_folder(path, include, exclude, client_paths.normalize_path("server/path"))
        self.assertFalse(added)

    def test_remove_folder(self):
        file_changes_json.init_file()
        path, include, exclude = h_get_dummy_folder_data()
        file_changes_json.add_folder(path, include, exclude, client_paths.normalize_path("server/path"))
        file_changes_json.remove_folder(path)
        data = file_changes_json._get_json_data()
        self.assertEqual({}, data)

    def test_remove_folder_not_existing(self):
        file_changes_json.init_file()
        path, include, exclude = h_get_dummy_folder_data()
        self.assertRaises(KeyError, file_changes_json.remove_folder, path, non_exists_ok=False)

    def test_set_include_regexes(self):
        file_changes_json.init_file()
        path, include, exclude = h_get_dummy_folder_data()
        file_changes_json.add_folder(path, include, exclude, client_paths.normalize_path("server/path"))

        new_include = ["hello", "you"]
        file_changes_json.set_include_regexes(path, new_include)
        folder = file_changes_json.get_folder_entry(path)
        self.assertEqual(new_include, folder["include_regexes"])

    def test_add_change_entry(self):
        file_changes_json.init_file()
        path, include, exclude = h_get_dummy_folder_data()
        file_changes_json.add_folder(path, include, exclude, client_paths.normalize_path("server/path"))

        rel_file_path = client_paths.normalize_path("test.txt")
        file_changes_json.add_change_entry(path, rel_file_path, gen_json.ACTION_PULL)
        folder_entry = file_changes_json.get_folder_entry(path)
        changes = folder_entry["changes"]
        self.assertEqual(1, len(changes))
