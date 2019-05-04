import unittest
from unittest.mock import patch
import json

from OpenDrive.server_side import file_changes_json as server_json
from OpenDrive.server_side import paths as server_paths
from OpenDrive import net_interface

from tests.client_side.helper_client import h_get_dummy_folder_data


def h_mock_set_json(data):
    json_path = server_json._get_file_path(1, 1)
    with open(json_path, "w") as f:
        json.dump(data, f)


def h_mock_get_json():
    json_path = server_json._get_file_path(1, 1)
    with open(json_path, "r") as f:
        return json.load(f)


get_json_module = "OpenDrive.server_side.file_changes_json._get_json_data"
set_json_module = "OpenDrive.server_side.file_changes_json._set_json_data"


class TestJson(unittest.TestCase):

    def setUp(self) -> None:
        server_json.create_changes_file_for_new_device(1, 1, empty=True)

    def test_init_file(self):
        server_json.create_changes_file_for_new_device(1, 1, empty=True)
        file_path = server_json._get_file_path(1, 1)
        with open(file_path, "r") as file:
            data = json.load(file)
            self.assertEqual([], data)

    @patch(get_json_module, h_mock_get_json)
    @patch(set_json_module, h_mock_set_json)
    def test_add_folder(self):
        path = server_paths.NormalizedPath("folder_1")
        server_json.add_folder(path)
        data = server_json._get_json_data()
        expected = [{"folder_path": path, "changes": []}]
        self.assertEqual(expected, data)

    def test_add_folder_existing(self):
        server_json.init_file()
        path, include, exclude = h_get_dummy_folder_data()
        added = server_json.add_folder(path, include, exclude)
        self.assertTrue(added)
        added = server_json.add_folder(path, include, exclude)
        self.assertFalse(added)

    def test_remove_folder(self):
        server_json.init_file()
        path, include, exclude = h_get_dummy_folder_data()
        server_json.add_folder(path, include, exclude)
        server_json.remove_folder(path)
        data = server_json._get_json_data()
        self.assertEqual([], data)

    def test_remove_folder_not_existing(self):
        server_json.init_file()
        path, include, exclude = h_get_dummy_folder_data()
        self.assertRaises(KeyError, server_json.remove_folder, path, non_exists_ok=False)

    def test_set_include_regexes(self):
        server_json.init_file()
        path, include, exclude = h_get_dummy_folder_data()
        server_json.add_folder(path, include, exclude)

        new_include = ["hello", "you"]
        server_json.set_include_regexes(path, new_include)
        folder = server_json.get_folder_entry(path)
        self.assertEqual(new_include, folder["include_regexes"])

    def test_add_change_entry(self):
        server_json.init_file()
        path, include, exclude = h_get_dummy_folder_data()
        server_json.add_folder(path, include, exclude)

        rel_file_path = client_paths.normalize_path("test.txt")
        server_json.add_change_entry(path, rel_file_path, server_json.CHANGE_CREATED,
                                     server_json.ACTION_PULL)
        server_json.add_change_entry(path, rel_file_path, server_json.CHANGE_MODIFIED,
                                     server_json.ACTION_PULL)
        folder_entry = server_json.get_folder_entry(path)
        changes = folder_entry["changes"]
        self.assertEqual(1, len(changes))
        self.assertEqual(2, len(changes[0]["changes"]))
