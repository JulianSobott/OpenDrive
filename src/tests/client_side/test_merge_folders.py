import unittest
import os

import general.merge_folders
from tests.client_side.helper_client import h_register_dummy_user_device_client
from tests.helper_all import h_stop_server_process, h_start_server_process, h_client_routine, h_create_empty

from OpenDrive.client_side import merge_folders
from OpenDrive.general.paths import normalize_path
from OpenDrive.client_side import paths as c_paths
from OpenDrive.server_side import paths as s_paths
from OpenDrive.client_side import synchronization as c_sync
from OpenDrive.client_side import interface
from OpenDrive.client_side import file_changes_json as c_json
from OpenDrive import net_interface


def h_create_files_folders(abs_dest_path: str, structure: dict, start_empty=False):
    """

    :param abs_dest_path: files and folders are created inside
    :param structure: A dict with the following structure:

        Folder:
            "folder_name": top_folder_name,
            "files": List[file_names]
            "folders": List[Folder]

    :param start_empty: removes everything that is already in the folder at the beginning
    :return: None
    """
    if start_empty:
        h_create_empty(abs_dest_path)

    def recursive_creation(inner_abs_path: str, folder: dict):
        try:
            os.mkdir(inner_abs_path)
        except FileExistsError:
            pass
        for file in folder["files"]:
            file_path = os.path.join(inner_abs_path, file)
            with open(file_path, "w"):
                pass
        for f in folder["folders"]:
            f_path = os.path.join(inner_abs_path, f["folder_name"])
            recursive_creation(f_path, f)

    return recursive_creation(abs_dest_path, structure)


class TestFolderWalker(unittest.TestCase):

    def setUp(self) -> None:
        self._server_process = h_start_server_process()

    def tearDown(self) -> None:
        h_stop_server_process(self._server_process)

    def test_walk(self):
        example_dict = {
            "folder_name": "top",
            "files": [{"file_name": "test.txt", "modified_timestamp": 1234}],
            "folders": [{"folder_name": "inner", "files": [{"file_name": "inner.txt", "modified_timestamp": 23}],
                         "folders": [
                             {"folder_name": "inner2", "files": [{"file_name": "inner2.txt", "modified_timestamp": 23}],
                              "folders": []}]},
                        ]
        }
        for dir_name, dirs, file_names in general.merge_folders.walk_directories(example_dict, normalize_path("")):
            print(f"parent_path: {dir_name}, dir_name: {dirs}, file_names: {file_names}")


class TestMergeMethods(unittest.TestCase):

    def setUp(self) -> None:
        self._server_process = h_start_server_process()

    def tearDown(self) -> None:
        h_stop_server_process(self._server_process)

    def h_test_merge_method(self, merge_method, f1_init_content, f2_init_content, expected_content,
                            yield_before_merge=False):
        c_json.init_file(empty=True)
        h_register_dummy_user_device_client()
        abs_local_path = normalize_path(c_paths.LOCAL_CLIENT_DATA, "folder1")
        h_create_empty(abs_local_path)
        f1_path = os.path.join(c_paths.LOCAL_CLIENT_DATA, "folder1")
        f2_path = s_paths.rel_user_path_to_abs("folder1", 1)
        net_interface.server.add_folder(f2_init_content["folder_name"])

        h_create_files_folders(f1_path, f1_init_content)
        h_create_files_folders(f2_path, f2_init_content)

        if yield_before_merge:
            yield

        interface.add_sync_folder(abs_local_path, "folder1", merge_method=merge_method)

        f1_structure = general.merge_folders.generate_content_of_folder(f1_path, only_files_list=True,
                                                                        top_folder_name=f1_init_content["folder_name"])
        f2_structure = general.merge_folders.generate_content_of_folder(f2_path, only_files_list=True,
                                                                        top_folder_name=f2_init_content["folder_name"])
        self.assertEqual(expected_content, f2_structure)
        self.assertEqual(expected_content, f1_structure)
        yield

    @h_client_routine(clear_folders=True)
    def test_take_1(self):
        f1_content = {"folder_name": "folder1", "files": ["test.txt", "test2.txt"], "folders": [
            {"folder_name": "inner1", "files": ["inner1_test.txt", "inner1_test2.txt"], "folders": []},
            {"folder_name": "inner2", "files": ["inner2_test.txt", "inner2_test2.txt"], "folders": []}
        ]}
        f2_content = {"folder_name": "folder1", "files": [], "folders": []}

        self.h_test_merge_method(merge_folders.MergeMethods.TAKE_1, f1_content, f2_content, f1_content)

    @h_client_routine(clear_folders=True)
    def test_take_2(self):
        f1_content = {"folder_name": "folder1", "files": [], "folders": []}
        f2_content = {"folder_name": "folder1", "files": ["test.txt", "test2.txt"], "folders": [
            {"folder_name": "inner1", "files": ["inner1_test.txt", "inner1_test2.txt"], "folders": []},
            {"folder_name": "inner2", "files": ["inner2_test.txt", "inner2_test2.txt"], "folders": []}
        ]}

        self.h_test_merge_method(merge_folders.MergeMethods.TAKE_2, f1_content, f2_content, f2_content)

    @h_client_routine(clear_folders=True)
    def test_prioritize_latest(self):
        f1_content = {"folder_name": "folder1", "files": ["f1.txt", "f2.txt"], "folders": []}
        f2_content = {"folder_name": "folder1", "files": ["f1.txt", "f2.txt", "f3.txt"], "folders": []}
        f1_path = os.path.join(c_paths.LOCAL_CLIENT_DATA, "folder1")
        f2_path = s_paths.rel_user_path_to_abs("folder1", 1)

        generator = self.h_test_merge_method(merge_folders.MergeMethods.PRIORITIZE_LATEST, f1_content, f2_content,
                                             f2_content, yield_before_merge=True)
        next(generator)
        with open(os.path.join(f1_path, "f1.txt"), "w") as f:
            f.write("New content in f1")
        with open(os.path.join(f2_path, "f2.txt"), "w") as f:
            f.write("New content in f2")
        next(generator)
        with open(os.path.join(f1_path, "f2.txt"), "r") as f:
            self.assertEqual("New content in f2", f.read().strip())
        with open(os.path.join(f2_path, "f1.txt"), "r") as f:
            self.assertEqual("New content in f1", f.read().strip())


class TestMerge(unittest.TestCase):
    def setUp(self) -> None:
        self._server_process = h_start_server_process()

    def tearDown(self) -> None:
        h_stop_server_process(self._server_process)

    @h_client_routine(clear_folders=True)
    def test_merge_folders(self):
        c_json.init_file(empty=True)
        h_register_dummy_user_device_client()
        abs_local_path = normalize_path(c_paths.LOCAL_CLIENT_DATA, "folder1")
        h_create_empty(abs_local_path)
        dummy_content = {"folder_name": "folder1", "files": ["test.txt", "test2.txt"], "folders": [
            {"folder_name": "inner1", "files": ["inner1_test.txt", "inner1_test2.txt"], "folders": []},
            {"folder_name": "inner2", "files": ["inner2_test.txt", "inner2_test2.txt"], "folders": []}
        ]}
        h_create_files_folders(abs_local_path, dummy_content)

        interface.add_sync_folder(abs_local_path, "folder1")

        server_path = s_paths.rel_user_path_to_abs("folder1", 1)
        current_structure = general.merge_folders.generate_content_of_folder(server_path, only_files_list=True,
                                                                             top_folder_name="folder1")
        expected_structure = dummy_content
        self.assertEqual(expected_structure, current_structure)
