import unittest
import os
import shutil

import OpenDrive.server_side.folders as folders
from OpenDrive.server_side import paths as server_paths
from OpenDrive.server_side import database
from tests.helper_all import h_clear_init_all_folders

from tests.server_side.helper_server import h_register_dummy_user_device


class TestFolders(unittest.TestCase):

    def setUp(self) -> None:
        h_clear_init_all_folders()
        self.user, device, token = h_register_dummy_user_device()

    def tearDown(self) -> None:
        pass

    def test_create_physical_folder(self):
        folder_name = "TestFolder"
        folders._create_physical_folder(self.user.user_id, folder_name)
        expected = os.path.join(server_paths.get_users_root_folder(self.user.user_id), folder_name)
        self.assertTrue(os.path.exists(expected))

    def test_add_folder(self):
        folder_name = "TestFolder"
        folders._add_folder_to_user(self.user.user_id, folder_name)
        expected = os.path.join(server_paths.get_users_root_folder(self.user.user_id), folder_name)
        self.assertTrue(os.path.exists(expected))
        folder_entry = database.Folder.get_by_user_and_name(self.user.user_id, folder_name)
        self.assertIsInstance(folder_entry, database.Folder)