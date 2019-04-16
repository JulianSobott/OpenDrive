import unittest
import os
import shutil
import pynetworking as net

from OpenDrive.general import paths as gen_paths
from OpenDrive.client_side import paths as client_paths
from OpenDrive.server_side import paths as server_paths
from OpenDrive import net_interface

from src.tests import client_server_environment as cs_env
from OpenDrive.general import file_exchanges


class TestFileExchanges(unittest.TestCase):

    def setUp(self) -> None:
        self._server_process = cs_env.start_server_process()
        self._dummy_client_folder = os.path.join(client_paths.LOCAL_CLIENT_DATA, "DUMMY_FOLDER")
        self._dummy_server_folder = os.path.join(server_paths.LOCAL_SERVER_DATA, "DUMMY_FOLDER")
        self.helper_clean_dummy_folders()
        self._file_name = "dummy.txt"
        self._dummy_file_path = self.helper_create_dummy_file()
        self._server = net_interface.ServerCommunicator.remote_functions

    def tearDown(self) -> None:
        cs_env.stop_process(self._server_process)

    def helper_create_dummy_file(self):
        path = os.path.join(self._dummy_client_folder, self._file_name)
        with open(path, "w+") as file:
            file.write("Hello" * 10)
        return path

    def helper_clean_dummy_folders(self):
        shutil.rmtree(self._dummy_client_folder, ignore_errors=True)
        shutil.rmtree(self._dummy_server_folder, ignore_errors=True)
        try:
            os.mkdir(self._dummy_client_folder)
        except FileExistsError:
            pass
        try:
            os.mkdir(self._dummy_server_folder)
        except FileExistsError:
            pass

    def test_get_file(self):
        abs_file_src_path = self._dummy_file_path
        abs_file_dest_path = os.path.join(self._dummy_server_folder, self._file_name)
        file: net.File = file_exchanges.get_file(abs_file_src_path, abs_file_dest_path)
        self.assertEqual(gen_paths.normalize_path(file.dst_path), gen_paths.normalize_path(abs_file_dest_path))

    def test_get_file_non_exist(self):
        abs_file_src_path = os.path.join(self._dummy_client_folder, "non_existing.txt")
        abs_file_dest_path = os.path.join(self._dummy_server_folder, self._file_name)
        self.assertRaises(FileNotFoundError, file_exchanges.get_file, abs_file_src_path, abs_file_dest_path)


if __name__ == '__main__':
    unittest.main()
