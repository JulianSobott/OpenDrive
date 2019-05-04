import unittest

from OpenDrive.client_side import synchronization as c_sync

from tests.helper_all import h_clear_init_all_folders, h_start_server_process, h_stop_server_process, h_client_routine
from tests.client_side.helper_client import h_register_dummy_user_device_client


class TestSynchronization(unittest.TestCase):

    def setUp(self) -> None:
        self._server_process = h_start_server_process()

    def tearDown(self) -> None:
        h_stop_server_process(self._server_process)

    @h_client_routine()
    def test_get_server_changes(self):
        h_register_dummy_user_device_client()
        changes = c_sync._get_server_changes()
        self.assertEqual([], changes)
