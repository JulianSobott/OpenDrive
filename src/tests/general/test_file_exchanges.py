import unittest
import os
from typing import Tuple

import pynetworking as net

from OpenDrive.general import paths as gen_paths
from OpenDrive import net_interface
from OpenDrive.general import file_exchanges

from tests.helper_all import h_clear_init_all_folders, h_start_server_process, h_stop_server_process, \
    h_clear_init_dummy_folders


def h_create_dummy_client_file(dummy_folder_path: str) -> Tuple[str, str]:
    file_name = "dummy.txt"
    path = os.path.join(dummy_folder_path, file_name)
    with open(path, "w+") as file:
        file.write("Hello" * 10)
    return file_name, path


class TestFileExchanges(unittest.TestCase):

    def setUp(self) -> None:
        h_clear_init_all_folders()
        self._server_process = h_start_server_process()
        self._dummy_client_folder, self._dummy_server_folder = h_clear_init_dummy_folders()
        self._file_name, self._dummy_file_path = h_create_dummy_client_file(self._dummy_client_folder)
        self._server = net_interface.ServerCommunicator.remote_functions

    def tearDown(self) -> None:
        h_stop_server_process(self._server_process)

    def test_get_file(self):
        abs_file_src_path = self._dummy_file_path
        abs_file_dest_path = os.path.join(self._dummy_server_folder, self._file_name)
        file: net.File = file_exchanges.get_file(abs_file_src_path, abs_file_dest_path)
        self.assertEqual(gen_paths.normalize_path(file.dst_path), gen_paths.normalize_path(abs_file_dest_path))

    def test_get_file_non_exist(self):
        abs_file_src_path = os.path.join(self._dummy_client_folder, "non_existing.txt")
        abs_file_dest_path = os.path.join(self._dummy_server_folder, self._file_name)
        self.assertRaises(FileNotFoundError, file_exchanges.get_file, abs_file_src_path, abs_file_dest_path)

    def test_move_file(self):
        abs_src_path = self._dummy_file_path
        abs_dest_path = os.path.join(self._dummy_server_folder, "new_name.txt")
        file_exchanges.move_file(abs_src_path, abs_dest_path)
        self.assertTrue(os.path.isfile(abs_dest_path))
        self.assertFalse(os.path.isfile(abs_src_path))

    def test_remove_file(self):
        abs_src_path = self._dummy_file_path
        file_exchanges.remove_file(abs_src_path)
        self.assertFalse(os.path.isfile(abs_src_path))


if __name__ == '__main__':
    unittest.main()
