import unittest
from unittest import mock

from src.tests import client_server_environment as cs_env
from OpenDrive import client_side, server_side


class TestAuthentication(unittest.TestCase):

    def setUp(self) -> None:
        self._server_process = cs_env.start_server_process()

    def tearDown(self) -> None:
        cs_env.stop_process(self._server_process)

    @cs_env.client_routine
    def test_register_user_device_cli(self):
        cs_env.delete_recreate_server_db()
        inputs = (in_val for in_val in ["RandomUsername", ""])

        def mock_input(prompt):
            return next(inputs)
        with mock.patch('builtins.input', mock_input), mock.patch("getpass.getpass", return_value="12Password34"):
            client_side.authentication.register_user_device_cli()


if __name__ == '__main__':
    unittest.main()
