import unittest
import os
import pynetworking as net

from OpenDrive.general import paths as gen_paths
from OpenDrive.server_side import paths as server_paths
from OpenDrive.server_side.file_exchanges import PullAction
from OpenDrive import net_interface

from tests.helper_all import h_clear_init_all_folders, h_client_routine, h_start_server_process, h_stop_server_process, \
    h_clear_init_dummy_folders
from tests.client_side.helper_client import h_register_dummy_user_device_client
from tests.client_side.test_authentication import TestAuthentication


def h_create_user_dummy_file():
    user_id = 1
    file_name = "dummy.txt"
    rel_path = os.path.join("DUMMY", file_name)
    path = os.path.join(server_paths.FOLDERS_ROOT, "user_" + str(user_id), rel_path)
    os.makedirs(os.path.split(path)[0], exist_ok=True)
    with open(path, "w+") as file:
        file.write("Hello" * 10)
    return rel_path


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


class TestActions(unittest.TestCase):

    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    @h_client_routine()
    def test_pull_action(self):
        abs_local_path = TestFileExchanges.helper_create_user_dummy_file(1, "File1.txt")
        abs_remote_path = gen_paths.LOCAL_DATA
        # action = PullAction()


if __name__ == '__main__':
    unittest.main()
