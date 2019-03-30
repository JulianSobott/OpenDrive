import unittest
from typing import Generator
from unittest import mock

from src.tests import client_server_environment as cs_env
from OpenDrive import client_side, server_side


def mock_input(inputs: Generator):
    def caller(prompt: str):
        return next(inputs)

    return caller


class TestAuthentication(unittest.TestCase):

    def setUp(self) -> None:
        self._server_process = cs_env.start_server_process()

    def tearDown(self) -> None:
        cs_env.stop_process(self._server_process)

    @cs_env.client_routine(clear_server_db=True)
    def test_register_user_device_cli(self):
        inputs = (in_val for in_val in ["RandomUsername", ""])

        with (mock.patch('builtins.input', mock_input(inputs)),
              mock.patch("getpass.getpass", return_value="12Password34")):
            client_side.authentication.register_user_device_cli()


if __name__ == '__main__':
    unittest.main()
