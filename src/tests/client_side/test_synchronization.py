import shutil
import unittest
from typing import Optional
import os

import general.file_exchanges
from OpenDrive.client_side import synchronization as c_sync
from OpenDrive.general import file_changes_json as gen_json
from OpenDrive.general import paths as gen_paths
from OpenDrive.server_side import paths as server_paths
from OpenDrive.client_side import paths as client_paths

from tests.helper_all import h_clear_init_all_folders, h_start_server_process, h_stop_server_process, h_client_routine
from tests.client_side.helper_client import h_register_dummy_user_device_client


def h_create_dummy_server_change_file():
    dummy_changes = {}
    rel_entry_path = gen_paths.NormalizedPath("test_1.txt")
    action_type = gen_json.ACTION_PULL
    is_dir = False
    new_file_path = None
    gen_json._add_new_change_entry(dummy_changes, rel_entry_path, action_type, is_dir, new_file_path)
    return dummy_changes.popitem()


def h_create_dummy_client_change_file():
    dummy_changes = {}
    rel_entry_path = gen_paths.NormalizedPath("test_1.txt")
    action_type = gen_json.ACTION_PULL
    is_dir = False
    new_file_path = None
    gen_json._add_new_change_entry(dummy_changes, rel_entry_path, action_type, is_dir, new_file_path)
    return dummy_changes.popitem()


def h_create_folder_entry(folder_path: gen_paths.NormalizedPath, changes: dict, client_side=False):
    if client_side:
        return {folder_path: {"changes": changes, "server_folder_path": folder_path}}
    else:
        return {folder_path: {"changes": changes}}


def h_create_changes(changes: list) -> dict:
    return {change["new_file_path"]: change for change in changes}


def h_create_change(rel_entry_path: gen_json.NormalizedPath, action: gen_json.ActionType, is_directory: bool = False,
                    new_file_path: gen_json.NormalizedPath = None):
    changes = {}
    gen_json._add_new_change_entry(changes, rel_entry_path, action, is_directory, new_file_path)
    if new_file_path:
        return h_create_changes([changes[new_file_path]])
    else:
        return h_create_changes([changes[rel_entry_path]])


def h_create_action(action: gen_json.ActionType, src_path: gen_paths.NormalizedPath,
                    dest_path: Optional[gen_paths.NormalizedPath] = None) -> general.file_exchanges.SyncAction:
    return c_sync._create_action(action, src_path, dest_path)


class TestSynchronization(unittest.TestCase):

    def setUp(self) -> None:
        self._server_process = h_start_server_process()

    def tearDown(self) -> None:
        h_stop_server_process(self._server_process)

    @h_client_routine()
    def test_get_server_changes(self):
        h_register_dummy_user_device_client()
        changes = c_sync._get_server_changes()
        self.assertEqual({}, changes)


class TestMerging(unittest.TestCase):

    def h_check_merge(self, server_changes, client_changes, expected_server, expected_client, expected_conflicts):
        server_actions, client_actions, conflicts = c_sync._merge_changes(server_changes, client_changes)
        self.assertEqual(expected_server, server_actions)
        self.assertEqual(expected_client, client_actions)
        self.assertEqual(expected_conflicts, conflicts)

    def test_merge_changes_create_client(self):
        client_changes = {**h_create_folder_entry(gen_paths.NormalizedPath("folder_1"),
                                                  {**h_create_change(gen_paths.NormalizedPath("test1.txt"),
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
                                                                     gen_json.ACTION_DELETE)},
                                                  client_side=True)}

        server_changes = h_create_folder_entry(gen_paths.NormalizedPath("folder_1"), {})

        expected_server = [h_create_action(gen_json.ACTION_DELETE, gen_paths.NormalizedPath("folder_1/test1.txt"))]
        expected_client = []
        expected_conflicts = []
        self.h_check_merge(server_changes, client_changes, expected_server, expected_client, expected_conflicts)

    def test_merge_changes_create_server(self):
        server_changes = {**h_create_folder_entry(gen_paths.NormalizedPath("folder_1"),
                                                  {**h_create_change(gen_paths.NormalizedPath("test1.txt"),
                                                                     gen_json.ACTION_PULL)}, client_side=False)}

        client_changes = h_create_folder_entry(gen_paths.NormalizedPath("folder_1"), {}, client_side=True)

        expected_server = []
        expected_client = [h_create_action(gen_json.ACTION_PULL, gen_paths.NormalizedPath("folder_1/test1.txt"),
                                           gen_paths.NormalizedPath("folder_1/test1.txt"))]
        expected_conflicts = []
        self.h_check_merge(server_changes, client_changes, expected_server, expected_client, expected_conflicts)

    def test_merge_changes_move_server(self):
        server_changes = {**h_create_folder_entry(gen_paths.NormalizedPath("folder_1"),
                                                  {**h_create_change(gen_paths.NormalizedPath("test1.txt"),
                                                                     gen_json.ACTION_MOVE,
                                                                     new_file_path=gen_paths.NormalizedPath(
                                                                         "test2.txt"))},
                                                  client_side=True)}

        client_changes = h_create_folder_entry(gen_paths.NormalizedPath("folder_1"), {}, client_side=True)

        expected_client = [h_create_action(gen_json.ACTION_MOVE, gen_paths.NormalizedPath("folder_1/test1.txt"),
                                           gen_paths.NormalizedPath("folder_1/test2.txt"))]
        expected_server = []
        expected_conflicts = []
        self.h_check_merge(server_changes, client_changes, expected_server, expected_client, expected_conflicts)

    def test_merge_changes_delete_server(self):
        server_changes = {**h_create_folder_entry(gen_paths.NormalizedPath("folder_1"),
                                                  {**h_create_change(gen_paths.NormalizedPath("test1.txt"),
                                                                     gen_json.ACTION_DELETE)},
                                                  client_side=True)}

        client_changes = h_create_folder_entry(gen_paths.NormalizedPath("folder_1"), {}, client_side=True)

        expected_client = [h_create_action(gen_json.ACTION_DELETE, gen_paths.NormalizedPath("folder_1/test1.txt"))]
        expected_server = []
        expected_conflicts = []
        self.h_check_merge(server_changes, client_changes, expected_server, expected_client, expected_conflicts)

    def test_merge_changes_conflicts(self):
        l_file_change = h_create_change(gen_paths.NormalizedPath("test1.txt"),
                                              gen_json.ACTION_PULL)
        server_changes = {**h_create_folder_entry(gen_paths.NormalizedPath("folder_1"),
                                                  {**h_create_change(gen_paths.NormalizedPath("test1.txt"),
                                                                     gen_json.ACTION_PULL)}, client_side=False)}

        client_changes = {**h_create_folder_entry(gen_paths.NormalizedPath("folder_1"),
                                                  {**h_create_change(gen_paths.NormalizedPath("test1.txt"),
                                                                     gen_json.ACTION_PULL)}, client_side=True)}

        expected_server = []
        expected_client = []
        expected_conflicts = [{"folders": ["folder_1", "folder_1"],
                               "rel_file_path": "test1.txt",
                               "local_file": l_file_change["test1.txt"],
                               "remote_file": l_file_change["test1.txt"]}]
        self.h_check_merge(server_changes, client_changes, expected_server, expected_client, expected_conflicts)


def h_setup_execution_env():
    server_folder = os.path.join(server_paths.FOLDERS_ROOT, 'user_1/folder1')
    h_register_dummy_user_device_client()
    os.makedirs(server_folder, exist_ok=True)
    server_file_path = os.path.join(server_folder, 'test.txt')
    with open(server_file_path, "w") as f:
        f.write("Hello" * 10)
    return server_folder


class TestExecution(unittest.TestCase):

    def setUp(self) -> None:
        self._server_process = h_start_server_process()

    def tearDown(self) -> None:
        h_stop_server_process(self._server_process)
        try:
            shutil.rmtree(self.server_folder)
        except:
            pass

    @h_client_routine()
    def test_execute_client_actions_pull(self):
        self.server_folder = h_setup_execution_env()

        client_dest_path = os.path.join(client_paths.LOCAL_CLIENT_DATA, "test.txt")
        client_actions = [h_create_action(gen_json.ACTION_PULL, gen_paths.NormalizedPath("folder1/test.txt"),
                                          gen_paths.normalize_path(client_dest_path))]
        c_sync._execute_client_actions(client_actions)
        self.assertTrue(os.path.isfile(client_dest_path))

    def test_execute_client_actions_move(self):
        client_src_path = os.path.join(client_paths.LOCAL_CLIENT_DATA, "test.txt")
        with open(client_src_path, "w") as f:
            f.write("Lorem ipsum "*10)
        client_dest_path = os.path.join(client_paths.LOCAL_CLIENT_DATA, "new_test.txt")
        client_actions = [h_create_action(gen_json.ACTION_MOVE, gen_paths.normalize_path(client_src_path),
                                          gen_paths.normalize_path(client_dest_path))]
        c_sync._execute_client_actions(client_actions)
        self.assertTrue(os.path.isfile(client_dest_path))

    def test_execute_client_actions_delete(self):
        client_src_path = os.path.join(client_paths.LOCAL_CLIENT_DATA, "test.txt")
        with open(client_src_path, "w") as f:
            f.write("Lorem ipsum " * 10)

        client_actions = [h_create_action(gen_json.ACTION_DELETE, gen_paths.normalize_path(client_src_path))]
        c_sync._execute_client_actions(client_actions)
        self.assertFalse(os.path.isfile(client_src_path))

    @h_client_routine()
    def test_execute_server_actions_pull(self):
        self.server_folder = h_setup_execution_env()

        client_src_path = os.path.join(client_paths.LOCAL_CLIENT_DATA, "test2.txt")
        with open(client_src_path, "w") as f:
            f.write("Lorem ipsum " * 10)

        server_dest_path = "folder1/test2.txt"
        server_actions = [h_create_action(gen_json.ACTION_PULL, gen_paths.normalize_path(client_src_path),
                                          gen_paths.normalize_path(server_dest_path))]
        c_sync._execute_server_actions(server_actions)
        expected_path = os.path.join(server_paths.FOLDERS_ROOT, "user_1", server_dest_path)
        self.assertTrue(os.path.isfile(expected_path))

    @h_client_routine()
    def test_execute_server_actions_move(self):
        self.server_folder = h_setup_execution_env()
        server_src_path = os.path.join("folder1", "test.txt")

        server_dest_path = os.path.join("folder1", "new_test.txt")
        server_actions = [h_create_action(gen_json.ACTION_MOVE, gen_paths.normalize_path(server_src_path),
                                          gen_paths.normalize_path(server_dest_path))]
        c_sync._execute_server_actions(server_actions)
        expected_path = os.path.join(self.server_folder, "new_test.txt")
        self.assertTrue(os.path.isfile(expected_path))

    @h_client_routine()
    def test_execute_server_actions_delete(self):
        self.server_folder = h_setup_execution_env()
        server_src_path = os.path.join("folder1", "test.txt")

        server_actions = [h_create_action(gen_json.ACTION_DELETE, gen_paths.normalize_path(server_src_path))]
        c_sync._execute_server_actions(server_actions)
        self.assertFalse(os.path.isfile(server_src_path))
