import unittest
from unittest.mock import patch
import json

from OpenDrive.server_side import file_changes_json as server_json
from OpenDrive.server_side import paths as server_paths
from OpenDrive.general import file_changes_json as gen_json
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


def h_mock_set_get_json(func):
    def wrapper(*args, **kwargs):
        gen_json._get_json_data = h_mock_get_json
        server_json._get_json_data = h_mock_get_json
        gen_json._set_json_data = h_mock_set_json
        server_json._set_json_data = h_mock_set_json
        ret_value = func(*args, **kwargs)
        return ret_value

    return wrapper

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

    @h_mock_set_get_json
    def test_add_folder(self):
        path = server_paths.NormalizedPath("folder_1")
        server_json.add_folder(path)
        data = server_json._get_json_data()
        expected = [{"folder_path": path, "changes": []}]
        self.assertEqual(expected, data)

    @h_mock_set_get_json
    def test_add_folder_existing(self):
        path = server_paths.NormalizedPath("folder_1")
        added = server_json.add_folder(path)
        self.assertTrue(added)
        added = server_json.add_folder(path)
        self.assertFalse(added)

    @h_mock_set_get_json
    def test_remove_folder(self):
        path = server_paths.NormalizedPath("folder_1")
        server_json.add_folder(path)
        server_json.remove_folder(path)
        data = server_json._get_json_data()
        self.assertEqual([], data)

    @h_mock_set_get_json
    def test_remove_folder_not_existing(self):
        path = server_paths.normalize_path("p1")
        self.assertRaises(KeyError, server_json.remove_folder, path, non_exists_ok=False)

    @h_mock_set_get_json
    def test_add_change_entry(self):
        path = server_paths.NormalizedPath("folder_1")
        server_json.add_folder(path)
        rel_file_path = server_paths.normalize_path("test.txt")
        server_json.add_change_entry(path, rel_file_path, gen_json.CHANGE_CREATED,
                                     gen_json.ACTION_PULL)
        server_json.add_change_entry(path, rel_file_path, gen_json.CHANGE_MODIFIED,
                                     gen_json.ACTION_PULL)
        folder_entry = gen_json.get_folder_entry(path)
        changes = folder_entry["changes"]
        self.assertEqual(1, len(changes))
        self.assertEqual(2, len(changes[0]["changes"]))
