import unittest
import os
import shutil

import OpenDrive.server_side.folders as folders
from OpenDrive.server_side import paths as server_paths
from OpenDrive.server_side import database
from tests.client_server_environment import clear_init_folders

from tests.server_side import test_authentication as server_auth


class TestFolders(unittest.TestCase):

    def setUp(self) -> None:
        clear_init_folders()
        shutil.rmtree(server_paths.FOLDERS_ROOT)
        os.makedirs(server_paths.FOLDERS_ROOT)
        self.user, device, token = server_auth.TestRegistration.helper_register_dummy_user_device()

    def tearDown(self) -> None:
        pass

    def test_create_physical_folder(self):
        folder_name = "TestFolder"
        folders._create_physical_folder(self.user, folder_name)
        expected = folders.get_users_root_folder(self.user).joinpath(folder_name)
        self.assertTrue(expected.exists())

    def test_add_folder(self):
        folder_name = "TestFolder"
        folders.add_folder(self.user, folder_name)
        expected = folders.get_users_root_folder(self.user).joinpath(folder_name)
        self.assertTrue(expected.exists())
        folder_entry = database.Folder.get_by_user_and_name(self.user.user_id, folder_name)
        self.assertIsInstance(folder_entry, database.Folder)