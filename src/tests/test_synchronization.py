"""
Test1:
------
- create file at client
- is file copied to server?

"""
import unittest
import os
import time

from OpenDrive.client_side import interface, file_changes, file_changes_json
from OpenDrive.client_side import paths as client_paths
from OpenDrive.server_side import paths as server_paths

from tests.client_side.helper_client import h_register_dummy_user_device_client
from tests.helper_all import h_client_routine, h_stop_server_process, h_start_server_process, h_create_empty, \
    h_clear_init_all_folders


class TestSynchronization(unittest.TestCase):

    def setUp(self) -> None:
        self._server_process = h_start_server_process()

    def tearDown(self) -> None:
        h_stop_server_process(self._server_process)

    @h_client_routine()
    def test_create_pull(self):
        # =============== SETUP ===================================
        file_changes_json.init_file(empty=True)
        file_changes.start_observing()
        user = h_register_dummy_user_device_client()
        abs_local_path = client_paths.normalize_path(client_paths.LOCAL_CLIENT_DATA, "folder1")
        h_create_empty(abs_local_path)
        interface.add_sync_folder(abs_local_path, "folder1")

        # ================= END SETUP ==============================
        file_path = os.path.join(abs_local_path, "dummy.txt")
        with open(file_path, "w") as f:
            f.write("Hello World")
        time.sleep(2)
        expected_path = os.path.join(server_paths.get_users_root_folder(user.user_id), "folder1/dummy.txt")
        self.assertTrue(os.path.exists(expected_path), "dummy file is not pulled to server!")
