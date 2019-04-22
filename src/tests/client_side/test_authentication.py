import unittest
from typing import Generator
from unittest import mock

from tests.server_side.test_folders import TestFolders
from tests.server_side import test_folders
from src.tests.helper_all import h_clear_init_all_folders
from tests.server_side import test_authentication as server_auth
from OpenDrive import client_side, server_side


def mock_input(inputs: Generator):
    def caller(prompt: str):
        return next(inputs)

    return caller


class TestAuthentication(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        h_clear_init_all_folders

    def setUp(self) -> None:
        self._server_process = cs_env.start_server_process()

    def tearDown(self) -> None:
        cs_env.stop_process(self._server_process)

    @staticmethod
    def helper_register_dummy_user_device():
        cs_env.clear_init_folders()
        server_auth.TestRegistration.helper_clear_database()
        client_side.authentication.register_user_device("ClientName", "whatanamazingpassword111")

    @cs_env.client_routine(clear_server_db=True)
    def test_register(self):
        status = client_side.interface.register("Paul", "12P3wÖ")
        self.assertTrue(status.was_successful())

    @cs_env.client_routine(clear_server_db=True)
    def test_login_manual(self):
        user, device, token = server_auth.TestRegistration.helper_register_dummy_user_device()
        status = client_side.interface.login_manual(user.username, user.password)
        self.assertTrue(status.was_successful())

    @cs_env.client_routine(clear_server_db=True)
    def test_logout(self):
        user, device, token = server_auth.TestRegistration.helper_register_dummy_user_device()
        client_side.authentication._save_received_token(token)
        client_side.interface.login_auto()
        status = client_side.interface.logout()
        self.assertTrue(status.was_successful())

    @cs_env.client_routine(clear_server_db=True)
    def test_register_user_device_cli(self):
        inputs = (in_val for in_val in ["RandomUsername", ""])

        with mock.patch('builtins.input', mock_input(inputs)), mock.patch("getpass.getpass",
                                                                          return_value="12Password34"):
            client_side.authentication.register_user_device_cli()

    @cs_env.client_routine(clear_server_db=True)
    def test_login_manual_user_device_cli(self):
        user, device, token = server_auth.TestRegistration.helper_register_dummy_user_device()
        inputs = (in_val for in_val in [user.username])
        with mock.patch('builtins.input', mock_input(inputs)), mock.patch("getpass.getpass",
                                                                          return_value=user.password):
            client_side.authentication.login_manual_user_device_cli()

    @cs_env.client_routine(clear_server_db=True)
    def test_login_auto(self):
        TestAuthentication.helper_register_dummy_user_device()
        status = client_side.interface.login_auto()
        self.assertTrue(status.was_successful())


if __name__ == '__main__':
    unittest.main()
