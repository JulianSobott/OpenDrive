import unittest
import networking as net
from thread_testing import get_num_non_dummy_threads

from OpenDrive import start_server, start_client, interface
from OpenDrive.Logging import logger

local_address = "127.0.0.1", 5000


class TestConnecting(unittest.TestCase):

    def test_server_client_connection(self):
        start_server.start_server(local_address)
        start_client.start_client(local_address)
        self.assertEqual(True, interface.ServerCommunicator.is_connected())
        start_client.stop_client()
        start_server.stop_server()
        self.assertEqual(1, get_num_non_dummy_threads())
