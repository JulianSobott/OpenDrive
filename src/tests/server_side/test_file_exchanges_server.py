import unittest
import os
import pynetworking as net

from OpenDrive.general import paths as gen_paths
from OpenDrive.client_side import paths as client_paths
from OpenDrive.server_side import paths as server_paths
from OpenDrive import net_interface

from tests.helper_all import h_client_routine, h_start_server_process, h_stop_server_process, \
    h_clear_init_dummy_folders
from tests.client_side.helper_client import h_register_dummy_user_device_client


def h_create_user_dummy_file():
    """OpenDrive/local/server_side/ROOT/user_1/DUMMY/dummy.txt"""
    user_id = 1
    file_name = "dummy.txt"
    rel_path = os.path.join("DUMMY", file_name)
    path = os.path.join(server_paths.FOLDERS_ROOT, "user_" + str(user_id), rel_path)
    os.makedirs(os.path.split(path)[0], exist_ok=True)
    with open(path, "w+") as file:
        file.write("Hello" * 10)
    return rel_path


def h_create_dummy_file(abs_folder: str, file_name: str) -> str:
    path = os.path.join(abs_folder, file_name)
    os.makedirs(os.path.split(path)[0], exist_ok=True)
    with open(path, "w+") as file:
        file.write("Hello" * 10)
    return path


class TestFileExchanges(unittest.TestCase):

    def setUp(self) -> None:
        self._server_process = h_start_server_process()
        _, self._dummy_server_folder = h_clear_init_dummy_folders()
        self._server = net_interface.ServerCommunicator.remote_functions

    def tearDown(self) -> None:
        h_stop_server_process(self._server_process)

    @h_client_routine()
    def test_get_file_network(self):
        h_register_dummy_user_device_client()
        rel_file_src_path = h_create_user_dummy_file()

        file_name = "test.txt"
        abs_file_dest_path = os.path.join(self._dummy_server_folder, file_name)
        file: net.File = self._server.get_file(rel_file_src_path, abs_file_dest_path)
        self.assertEqual(gen_paths.normalize_path(file.dst_path), gen_paths.normalize_path(abs_file_dest_path))
        self.assertTrue(os.path.isfile(abs_file_dest_path))

    @h_client_routine()
    def test_get_file_non_exist_network(self):
        h_register_dummy_user_device_client()
        rel_file_src_path = os.path.join(server_paths.FOLDERS_ROOT, "user_1", "Not/Existing.txt")

        file_name = "NON_existing.txt"
        abs_file_dest_path = os.path.join(self._dummy_server_folder, file_name)
        self.assertRaises(FileNotFoundError, self._server.get_file, rel_file_src_path, abs_file_dest_path)

    @h_client_routine()
    def test_move_file(self):
        """Move: user_1/DUMMY/dummy.txt -> user_1/folder_2/file.txt"""
        h_register_dummy_user_device_client()

        rel_src_path = h_create_user_dummy_file()
        rel_dest_path = "folder_2/file.txt"
        self._server.move_file(rel_src_path, rel_dest_path)

        abs_src_path = os.path.join(server_paths.FOLDERS_ROOT, "user_1", rel_src_path)
        abs_dest_path = os.path.join(server_paths.FOLDERS_ROOT, "user_1", rel_dest_path)
        self.assertFalse(os.path.isfile(abs_src_path))
        self.assertTrue(os.path.isfile(abs_dest_path))

    @h_client_routine()
    def test_remove_file(self):
        """Remove: user_1/DUMMY/dummy.txt"""
        h_register_dummy_user_device_client()

        rel_src_path = h_create_user_dummy_file()
        self._server.remove_file(rel_src_path)

        abs_src_path = os.path.join(server_paths.FOLDERS_ROOT, "user_1", rel_src_path)
        self.assertFalse(os.path.isfile(abs_src_path))


if __name__ == '__main__':
    unittest.main()
