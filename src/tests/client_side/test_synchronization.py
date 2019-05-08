import unittest
from typing import Optional

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


def h_create_folder_entry(folder_path: gen_paths.NormalizedPath, changes: dict, client_side=False):
    if client_side:
        return {folder_path: {"changes": changes, "server_folder_path": folder_path}}
    else:
        return {folder_path: {"changes": changes}}


def h_create_changes(changes: list) -> dict:
    return {change["new_file_path"]: change for change in changes}


def h_create_change(rel_entry_path: gen_json.NormalizedPath, change_type: gen_json.ChangeType,
                    action: gen_json.ActionType, is_directory: bool = False,
                    new_file_path: gen_json.NormalizedPath = None):
    changes = {}
    gen_json._add_new_change_entry(changes, rel_entry_path, change_type, action, is_directory, new_file_path)
    if new_file_path:
        return h_create_changes([changes[new_file_path]])
    else:
        return h_create_changes([changes[rel_entry_path]])


def h_create_action(action: gen_json.ActionType, src_path: gen_paths.NormalizedPath,
                    dest_path: Optional[gen_paths.NormalizedPath] = None) -> c_sync.SyncAction:
    return c_sync._create_action(action, src_path, dest_path)


class TestSynchronization(unittest.TestCase):

    def setUp(self) -> None:
        self._server_process = h_start_server_process()

    def tearDown(self) -> None:
        h_stop_server_process(self._server_process)

    def h_check_merge(self, server_changes, client_changes, expected_server, expected_client, expected_conflicts):
        server_actions, client_actions, conflicts = c_sync._merge_changes(server_changes, client_changes)
        self.assertEqual(expected_server, server_actions)
        self.assertEqual(expected_client, client_actions)
        self.assertEqual(expected_conflicts, conflicts)

    @h_client_routine()
    def test_get_server_changes(self):
        h_register_dummy_user_device_client()
        changes = c_sync._get_server_changes()
        self.assertEqual([], changes)

    def test_merge_changes_create_client(self):
        client_changes = {**h_create_folder_entry(gen_paths.NormalizedPath("folder_1"),
                                                  {**h_create_change(gen_paths.NormalizedPath("test1.txt"),
                                                                     gen_json.CHANGE_CREATED,
                                                                     gen_json.ACTION_PULL)}, client_side=True)}

        server_changes = h_create_folder_entry(gen_paths.NormalizedPath("folder_1"), {})

        expected_server = [h_create_action(gen_json.ACTION_PULL, gen_paths.NormalizedPath("folder_1/test1.txt"),
                                           gen_paths.NormalizedPath("folder_1/test1.txt"))]
        expected_client = []
        expected_conflicts = []
        self.h_check_merge(server_changes, client_changes, expected_server, expected_client, expected_conflicts)

    def test_merge_changes_move_client(self):
        client_changes = {**h_create_folder_entry(gen_paths.NormalizedPath("folder_1"),
                                                  {**h_create_change(gen_paths.NormalizedPath("test1.txt"),
                                                                     gen_json.CHANGE_MOVED,
                                                                     gen_json.ACTION_MOVE,
                                                                     new_file_path=gen_paths.NormalizedPath(
                                                                         "test2.txt"))},
                                                  client_side=True)}

        server_changes = h_create_folder_entry(gen_paths.NormalizedPath("folder_1"), {})

        expected_server = [h_create_action(gen_json.ACTION_MOVE, gen_paths.NormalizedPath("folder_1/test1.txt"),
                                           gen_paths.NormalizedPath("folder_1/test2.txt"))]
        expected_client = []
        expected_conflicts = []
        self.h_check_merge(server_changes, client_changes, expected_server, expected_client, expected_conflicts)

    def test_merge_changes_delete_client(self):
        client_changes = {**h_create_folder_entry(gen_paths.NormalizedPath("folder_1"),
                                                  {**h_create_change(gen_paths.NormalizedPath("test1.txt"),
                                                                     gen_json.CHANGE_DELETED,
                                                                     gen_json.ACTION_DELETE)},
                                                  client_side=True)}

        server_changes = h_create_folder_entry(gen_paths.NormalizedPath("folder_1"), {})

        expected_server = [h_create_action(gen_json.ACTION_DELETE, gen_paths.NormalizedPath("folder_1/test1.txt"))]
        expected_client = []
        expected_conflicts = []
        self.h_check_merge(server_changes, client_changes, expected_server, expected_client, expected_conflicts)
