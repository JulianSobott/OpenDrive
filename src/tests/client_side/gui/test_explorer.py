from unittest import TestCase
import os

from OpenDrive.client_side import file_changes
from OpenDrive.client_side import file_changes_json
from OpenDrive.client_side import paths as client_paths
from OpenDrive.client_side import gui


def h_watch_dummy_folder(folder_name: str):
    abs_path = os.path.join(client_paths.LOCAL_CLIENT_DATA, folder_name)
    os.makedirs(abs_path, exist_ok=True)
    file_changes.add_folder(abs_path)


class TestExplorer(TestCase):

    def setUp(self) -> None:
        file_changes_json.init_file(empty=True)
        h_watch_dummy_folder("folder_1")
        h_watch_dummy_folder("folder_2")

    def simulate_remove_folder(self):
        gui.main.main()
