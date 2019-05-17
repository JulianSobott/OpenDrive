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

    # TODO: Add tests


if __name__ == '__main__':
    unittest.main()
