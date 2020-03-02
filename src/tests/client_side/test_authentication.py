import unittest
from typing import Generator
from unittest import mock
from pynetworking import client, server
import pynetworking.core.Communication_general

from OpenDrive import client_side
from OpenDrive import net_interface
from tests.client_side.helper_client import h_register_dummy_user_device_client
from OpenDrive.general.database import Token
from OpenDrive.client_side.program_state import is_authenticated_at_server, set_authenticated_at_server
from tests.helper_all import h_clear_init_all_folders, MockFile


class TestAuthentication(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        h_clear_init_all_folders()
        net_interface.ServerCommunicator.is_connected = mock.MagicMock(return_value=True)

    def setUp(self) -> None:
        set_authenticated_at_server(False)

    def test_register_success(self):
        token = Token()
        mock_server_call(token)
        with MockFile() as m:
            status = client_side.authentication.register_user_device("Paul", "12P3wÖ")
            self.assertTrue(status.was_successful())
            m.assert_called_once_with(str(token))
        self.assertTrue(is_authenticated_at_server())

    def test_register_fail(self):
        fail_msg = "Mock: Register failed"
        mock_server_call(fail_msg)
        status = client_side.authentication.register_user_device("Paul", "us")
        self.assertFalse(status.was_successful())
        self.assertEqual(fail_msg, status.get_text())
        self.assertFalse(is_authenticated_at_server())

    def test_login_manual_success(self):
        token = Token()
        mock_server_call(token)
        with MockFile() as m:
            status = client_side.authentication.login_manual("Ha", "ha")
            self.assertTrue(status.was_successful())
            m.assert_called_once_with(str(token))
            self.assertTrue(is_authenticated_at_server())

    def test_login_manual_fail(self):
        fail_msg = "Mock: login failed"
        mock_server_call(fail_msg)
        status = client_side.authentication.login_manual("Ha", "hup")
        self.assertFalse(status.was_successful())
        self.assertEqual(status.get_text(), fail_msg)
        self.assertFalse(is_authenticated_at_server())

    def test_logout(self):
        mock_server_call("")
        set_authenticated_at_server(True)
        status = client_side.authentication.logout()
        self.assertFalse(is_authenticated_at_server())
        self.assertTrue(status.was_successful())

    def test_register_user_device_cli(self):
        inputs = (in_val for in_val in ["RandomUsername", ""])
        mock_server_call(Token())
        with mock.patch('builtins.input', mock_input(inputs)), mock.patch("getpass.getpass",
                                                                          return_value="12Password34"):
            client_side.authentication.register_user_device_cli()

    def test_login_manual_user_device_cli(self):
        inputs = (v for v in ["Hans"])
        mock_server_call(Token())
        with mock.patch('builtins.input', mock_input(inputs)), mock.patch("getpass.getpass",
                                                                          return_value="Hello"):
            client_side.authentication.login_manual_user_device_cli()

    def test_login_auto_success(self):
        token = Token()
        with mock.patch("OpenDrive.client_side.authentication._get_token", mock.Mock(return_value=token)):
            mock_server_call(True)
            status = client_side.authentication.login_auto()
            self.assertTrue(status.was_successful())
            self.assertTrue(is_authenticated_at_server())

    def test_login_auto_fail_no_token(self):
        token = None
        with mock.patch("OpenDrive.client_side.authentication._get_token", mock.Mock(return_value=token)):
            status = client_side.authentication.login_auto()
            self.assertFalse(status.was_successful())
            self.assertFalse(is_authenticated_at_server())

    def test_login_auto_fail_invalid_token(self):
        token = Token()
        with mock.patch("OpenDrive.client_side.authentication._get_token", mock.Mock(return_value=token)):
            mock_server_call(False)
            status = client_side.authentication.login_auto()
            self.assertFalse(status.was_successful())
            self.assertFalse(is_authenticated_at_server())

    def test_get_token_success(self):
        expected_token = Token()
        with MockFile(read_data=str(expected_token)) as m:
            token = client_side.authentication._get_token()
            self.assertEqual(expected_token, token)

    def test_get_token_fail(self):
        with mock.patch("builtins.open", side_effect=FileNotFoundError):
            token = client_side.authentication._get_token()
            self.assertIsNone(token)

    def test_connection_needed_connected(self):
        with mock.patch("OpenDrive.net_interface.ServerCommunicator.is_connected", mock.MagicMock(return_value=True)):
            msg = "MOCK SUCCESS"
            res = client_side.authentication.connection_needed(lambda: msg)()
            self.assertEqual(msg, res)

    def test_connection_needed_disconnected(self):
        with mock.patch("OpenDrive.net_interface.ServerCommunicator.is_connected", mock.MagicMock(return_value=False)):
            res = client_side.authentication.connection_needed(lambda: "Message")()
            self.assertFalse(res.was_successful())


def mock_input(inputs: Generator):
    def caller(prompt: str):
        return next(inputs)

    return caller


def mock_server_call(return_value):
    def dummy(*args, **kwargs):
        def func(*args1, **kwargs1):
            return return_value
        return func
    pynetworking.core.Communication_general.MetaFunctionCommunicator.__getattribute__ = dummy
