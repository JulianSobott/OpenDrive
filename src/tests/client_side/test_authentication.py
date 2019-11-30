import unittest
from typing import Generator
from unittest import mock

from OpenDrive import client_side
from tests.client_side.helper_client import h_register_dummy_user_device_client
from tests.helper_all import h_clear_init_all_folders, h_start_server_process, h_stop_server_process, h_client_routine


def mock_input(inputs: Generator):
    def caller(prompt: str):
        return next(inputs)

    return caller


class TestAuthentication(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        h_clear_init_all_folders()

    def setUp(self) -> None:
        self._server_process = h_start_server_process()

    def tearDown(self) -> None:
        h_stop_server_process(self._server_process)

    @h_client_routine(clear_server_db=True)
    def test_register(self):
        status = client_side.interface.register("Paul", "12P3wÖ")
        self.assertTrue(status.was_successful())

    @h_client_routine(clear_server_db=True)
    def test_login_manual(self):
        user = h_register_dummy_user_device_client()
        status = client_side.interface.login_manual(user.username, user.password)
        self.assertTrue(status.was_successful())

    @h_client_routine(clear_server_db=True)
    def test_logout(self):
        h_register_dummy_user_device_client()
        client_side.interface.login_auto()
        status = client_side.interface.logout()
        self.assertTrue(status.was_successful())

    @h_client_routine(clear_server_db=True)
    def test_register_user_device_cli(self):
        inputs = (in_val for in_val in ["RandomUsername", ""])

        with mock.patch('builtins.input', mock_input(inputs)), mock.patch("getpass.getpass",
                                                                          return_value="12Password34"):
            client_side.authentication.register_user_device_cli()

    @h_client_routine(clear_server_db=True)
    def test_login_manual_user_device_cli(self):
        user = h_register_dummy_user_device_client()
        inputs = (in_val for in_val in [user.username])
        with mock.patch('builtins.input', mock_input(inputs)), mock.patch("getpass.getpass",
                                                                          return_value=user.password):
            client_side.authentication.login_manual_user_device_cli()

    @h_client_routine(clear_server_db=True)
    def test_login_auto(self):
        h_register_dummy_user_device_client()
        status = client_side.interface.login_auto()
        self.assertTrue(status.was_successful())


if __name__ == '__main__':
    import pyprofiling
    pyprofiling.profile(unittest.main, globals(), "OpenDrive", "authentication")
