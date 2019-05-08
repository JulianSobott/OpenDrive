import unittest

from OpenDrive.client_side import synchronization as c_sync
from OpenDrive.general import file_changes_json as gen_json
from OpenDrive.general import paths as gen_paths

from tests.helper_all import h_clear_init_all_folders, h_start_server_process, h_stop_server_process, h_client_routine
from tests.client_side.helper_client import h_register_dummy_user_device_client


def h_create_dummy_server_change_file():
    dummy_changes = {}
    rel_entry_path = gen_paths.NormalizedPath("test_1.txt")
    change_type = gen_json.CHANGE_CREATED
    action_type = gen_json.ACTION_PULL
    is_dir = False
    new_file_path = None
    gen_json._add_new_change_entry(dummy_changes, rel_entry_path, change_type, action_type, is_dir, new_file_path)
    return dummy_changes.popitem()


def h_create_dummy_client_change_file():
    dummy_changes = {}
    rel_entry_path = gen_paths.NormalizedPath("test_1.txt")
    change_type = gen_json.CHANGE_CREATED
    action_type = gen_json.ACTION_PULL
    is_dir = False
    new_file_path = None
    gen_json._add_new_change_entry(dummy_changes, rel_entry_path, change_type, action_type, is_dir, new_file_path)
    return dummy_changes.popitem()


def h_create_dummy_client_change_file():
    pass


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

    def test_merge_file_changes_only_client(self):
        server_file = None
        client_path, client_file = h_create_dummy_client_change_file()
        needed_server_actions, needed_client_actions, conflicts = c_sync._merge_file_changes(server_file, client_file)
        # expected_server = c_sync._create_action(gen_json.ACTION_PULL,
        #                                         client_path,
        #                                         )
        # self.assertEqual(, needed_server_actions)
