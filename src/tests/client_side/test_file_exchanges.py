import unittest
import os
import pynetworking as net

from OpenDrive import net_interface

from tests.client_side.helper_client import h_create_client_dummy_file
from tests.helper_all import h_client_routine, h_start_server_process, h_stop_server_process, \
    h_clear_init_dummy_folders
from tests.client_side.helper_client import h_register_dummy_user_device_client
from tests.od_logging import logger


class TestFileExchanges(unittest.TestCase):

    def setUp(self) -> None:
        self._server_process = h_start_server_process()
        _, self._dummy_server_folder = h_clear_init_dummy_folders()
        self._server = net_interface.server

    def tearDown(self) -> None:
        h_stop_server_process(self._server_process)

    @h_client_routine()
    def test_get_file_network(self):
        """Test FAIL"""
        h_register_dummy_user_device_client()
        abs_file_src_path = h_create_client_dummy_file()

        def h_simulate_get_file(abs_src, abs_dest):
            client: net_interface.ClientCommunicator = net.ClientManager().get()
            file = client.remote_functions.get_file(abs_src, abs_dest)
            return file.dst_path

        file_name = "test.txt"
        abs_file_dest_path = os.path.join(self._dummy_server_folder, file_name)
        ret = net_interface.server.h_execute_function(h_simulate_get_file, abs_file_src_path, abs_file_dest_path)
        logger.debug(ret)
        self.assertTrue(os.path.isfile(abs_file_dest_path))

    @h_client_routine()
    def test_get_file_non_exist_network(self):
        pass


if __name__ == '__main__':
    unittest.main()