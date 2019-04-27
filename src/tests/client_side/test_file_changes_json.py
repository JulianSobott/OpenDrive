import unittest
import json

from OpenDrive.client_side import file_changes_json


class TestJson(unittest.TestCase):

    def test_init_file(self):
        file_changes_json.init_file()
        with open(file_changes_json.client_paths.LOCAL_JSON_PATH, "r") as file:
            data = json.load(file)
            self.assertEqual([], data)