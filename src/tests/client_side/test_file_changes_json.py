import unittest
import json

from OpenDrive.client_side import file_changes_json
from OpenDrive.client_side import paths as client_paths


def h_get_dummy_folder():
    path = client_paths.LOCAL_CLIENT_DATA
    include = [".*"]
    exclude = []
    return path, include, exclude


class TestJson(unittest.TestCase):

    def test_init_file(self):
        file_changes_json.init_file()
        with open(client_paths.LOCAL_JSON_PATH, "r") as file:
            data = json.load(file)
            self.assertEqual([], data)

    def test_add_folder(self):
        path, include, exclude = h_get_dummy_folder()
        file_changes_json.add_folder(path, include, exclude)
        data = file_changes_json._get_json_data()
        expected = [{"folder_path": path, "include_regexes": include, "exclude_regexes": exclude, "changes": []}]
        self.assertEqual(expected, data)

    def test_add_folder_existing(self):
        file_changes_json.init_file()
        path, include, exclude = h_get_dummy_folder()
        added = file_changes_json.add_folder(path, include, exclude)
        self.assertTrue(added)
        added = file_changes_json.add_folder(path, include, exclude)
        self.assertFalse(added)
