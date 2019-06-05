import unittest
import threading
import os
import time

from OpenDrive.client_side import main
from OpenDrive.client_side import paths as client_paths
from OpenDrive.client_side import interface
from OpenDrive.client_side import file_changes_json as c_json

from OpenDrive.server_side import paths as server_paths
from tests.client_side.helper_client import h_register_dummy_user_device_client
from tests.helper_all import h_client_routine, h_start_server_process, h_stop_server_process, \
    h_clear_init_all_folders, h_create_empty


class TestMain(unittest.TestCase):

    def setUp(self) -> None:
        h_clear_init_all_folders()
        self._server_process = h_start_server_process()
        self.folder1_abs_local_path = client_paths.normalize_path(client_paths.LOCAL_CLIENT_DATA, "folder1")
        h_create_empty(self.folder1_abs_local_path)
        main.MIN_UPDATE_PAUSE_TIME = 1

    def tearDown(self) -> None:
        h_stop_server_process(self._server_process)

    @h_client_routine(clear_folders=False)
    def test_start_logged_in(self):
        user = h_register_dummy_user_device_client()
        main_thread = threading.Thread(target=main.start, daemon=True)
        main_thread.start()
        time.sleep(1)   # wait till changes.json is created

        interface.add_sync_folder(self.folder1_abs_local_path, "folder1")
        expected_content = c_json.get_all_data()
        file_path = os.path.join(self.folder1_abs_local_path, "dummy.txt")
        with open(file_path, "w") as f:
            f.write("Hello World")
        time.sleep(2)   # wait till synchronization finished
        expected_path = os.path.join(server_paths.get_users_root_folder(user.user_id), "folder1/dummy.txt")
        self.assertTrue(os.path.exists(expected_path), "dummy file is not pulled to server!")
        self.assertEqual(expected_content, c_json.get_all_data())
        time.sleep(1)   # wait till waiting...
        main.shutdown()
