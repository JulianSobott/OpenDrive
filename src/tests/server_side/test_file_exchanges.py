import unittest
import os
import pynetworking as net

from server_side.file_exchanges import PullAction
from tests import client_server_environment as cs_env
from tests.general import test_file_exchanges as gen_test_file_exchanges
from tests.client_side.test_authentication import TestAuthentication

from OpenDrive.general import paths as gen_paths
from OpenDrive.server_side import paths as server_paths


class TestFileExchanges(gen_test_file_exchanges.TestFileExchanges):

    def helper_setup(self):
        TestAuthentication.helper_register_dummy_user_device()
        self._rel_file_src_path = os.path.join("DummyFolder1", self._file_name)
        self.helper_create_user_dummy_file(1, self._rel_file_src_path)

    @staticmethod
    def helper_create_user_dummy_file(user_id: int, rel_file_path: str):
        path = os.path.join(server_paths.FOLDERS_ROOT, "user_" + str(user_id), rel_file_path)
        os.makedirs(os.path.split(path)[0], exist_ok=True)
        with open(path, "w+") as file:
            file.write("Hello" * 10)
        return path

    @cs_env.client_routine()
    def test_get_file(self):
        self.helper_setup()
        abs_file_dest_path = os.path.join(self._dummy_server_folder, self._file_name)
        file: net.File = self._server.get_file(self._rel_file_src_path, abs_file_dest_path)
        self.assertEqual(gen_paths.normalize_path(file.dst_path), gen_paths.normalize_path(abs_file_dest_path))
        self.assertTrue(os.path.isfile(abs_file_dest_path))

    @cs_env.client_routine()
    def test_get_file_non_exist(self):
        self.helper_setup()
        abs_file_dest_path = os.path.join(self._dummy_server_folder, self._file_name)
        rel_file_path = "HA.txt"
        self.assertRaises(FileNotFoundError, self._server.get_file, rel_file_path, abs_file_dest_path)


class TestActions(unittest.TestCase):

    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    @cs_env.client_routine()
    def test_pull_action(self):
        abs_local_path = TestFileExchanges.helper_create_user_dummy_file(1, "File1.txt")
        abs_remote_path = gen_paths.LOCAL_DATA
        action = PullAction()
