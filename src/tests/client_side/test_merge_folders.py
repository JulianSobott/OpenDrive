import unittest

from OpenDrive.client_side import merge_folders


class TestFolderWalker(unittest.TestCase):

    def test_walk(self):
        root_folder = "ROOT"
        example_dict = {
            "folder_name": "top",
            "files": [{"file_name": "test.txt", "modified_timestamp": 1234}],
            "folders": [{"folder_name": "inner", "files": [{"file_name": "inner.txt", "modified_timestamp": 23}],
                         "folders": []},
                        ]
        }
        for dir_name, dirs, file_names in merge_folders.walk_directories(example_dict):
            print(f"dir: {dir_name}, dirs: {dirs}, file_names: {file_names}")
