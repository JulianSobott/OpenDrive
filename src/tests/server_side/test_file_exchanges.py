import unittest
import shutil
from typing import Optional
import os

from OpenDrive import net_interface

from OpenDrive.general import paths as gen_paths
from OpenDrive.client_side import synchronization as c_sync
from OpenDrive.general import file_changes_json as gen_json
from OpenDrive.client_side import paths as client_paths
from OpenDrive.server_side import paths as server_paths

from tests.helper_all import h_create_empty, h_start_server_process, h_stop_server_process, h_client_routine, \
    h_clear_init_all_folders
from tests.client_side.helper_client import h_register_dummy_user_device_client


def h_fill_dummy_dir(abs_path: str):
    """Create dummy folders and files inside the path"""
    i1 = os.path.join(abs_path, "inner1")
    i2 = os.path.join(abs_path, "inner2")
    os.makedirs(i1, exist_ok=True)
    os.makedirs(i2, exist_ok=True)
    with open(os.path.join(i1, "test_inner.txt"), "w") as f:
        f.write("Hello World")
    with open(os.path.join(abs_path, "test.txt"), "w") as f:
        f.write("Hello World ROOT")


class TestPullDir(unittest.TestCase):

    def setUp(self) -> None:
        h_clear_init_all_folders()
        self._server_process = h_start_server_process()

    def tearDown(self) -> None:
        h_stop_server_process(self._server_process)

    @h_client_routine()
    def test_pull_dir_client_to_server(self):
        """Copy dir from client to server"""
        h_register_dummy_user_device_client()
        client_folder = gen_paths.normalize_path(client_paths.LOCAL_CLIENT_DATA, "folder1")
        h_fill_dummy_dir(client_folder)
        actions = [c_sync.create_action(gen_paths.normalize_path("folder1"),
                                        gen_paths.normalize_path(""),
                                        gen_json.ACTION_PULL,
                                        remote_abs_path=client_folder,
                                        is_directory=True)]
        net_interface.server.execute_actions(actions)
        self.assertTrue(os.path.exists((server_paths.rel_user_path_to_abs("folder1", 1))))
        self.assertTrue(os.path.exists((server_paths.rel_user_path_to_abs("folder1/inner1", 1))))
        self.assertTrue(os.path.exists((server_paths.rel_user_path_to_abs("folder1/inner2", 1))))
        self.assertTrue(os.path.exists((server_paths.rel_user_path_to_abs("folder1/inner1/test_inner.txt", 1))))
        self.assertTrue(os.path.exists((server_paths.rel_user_path_to_abs("folder1/test.txt", 1))))

    @h_client_routine()
    def test_pull_dir_server_to_client(self):
        """Copy dir from server to client"""
        h_register_dummy_user_device_client()
        server_folder = gen_paths.normalize_path(server_paths.rel_user_path_to_abs("folder1", 1))
        client_folder = gen_paths.normalize_path(client_paths.LOCAL_CLIENT_DATA, "folder1")
        h_fill_dummy_dir(server_folder)
        net_interface.server.get_dir("folder1", client_folder)
        self.assertTrue(os.path.exists((os.path.join(client_folder))))
        self.assertTrue(os.path.exists((os.path.join(client_folder, "inner1"))))
        self.assertTrue(os.path.exists((os.path.join(client_folder, "inner2"))))
        self.assertTrue(os.path.exists((os.path.join(client_folder, "inner1/test_inner.txt"))))
        self.assertTrue(os.path.exists((os.path.join(client_folder, "test.txt"))))


if __name__ == '__main__':
    unittest.main()
