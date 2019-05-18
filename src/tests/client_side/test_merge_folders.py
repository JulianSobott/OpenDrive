import unittest

from OpenDrive.client_side import merge_folders
from general.paths import normalize_path


class TestFolderWalker(unittest.TestCase):

    def test_walk(self):
        example_dict = {
            "folder_name": "top",
            "files": [{"file_name": "test.txt", "modified_timestamp": 1234}],
            "folders": [{"folder_name": "inner", "files": [{"file_name": "inner.txt", "modified_timestamp": 23}],
                         "folders": [
                             {"folder_name": "inner2", "files": [{"file_name": "inner2.txt", "modified_timestamp": 23}],
                              "folders": []}]},
                        ]
        }
        for dir_name, dirs, file_names in merge_folders.walk_directories(example_dict, normalize_path("")):
            print(f"parent_path: {dir_name}, dir_name: {dirs}, file_names: {file_names}")
