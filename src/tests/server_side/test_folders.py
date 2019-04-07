import unittest
import os

import OpenDrive.server_side.folders as folders
from OpenDrive.server_side import paths as server_paths

from tests.server_side import test_authentication as server_auth


class TestFolders(unittest.TestCase):

    def setUp(self) -> None:
        self.user, device, token = server_auth.TestRegistration.helper_register_dummy_user_device()

    def tearDown(self) -> None:
        pass

    def test_create_physical_folder(self):
        folder_name = "TestFolder"
        folders._create_physical_folder(self.user.user_id, folder_name)
        expected = os.path.join(server_paths.FOLDERS_ROOT, f"user_{self.user.user_id}", folder_name)
        self.assertTrue(os.path.exists(expected))
