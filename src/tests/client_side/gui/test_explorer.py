import threading
from unittest import TestCase
import os

from OpenDrive.client_side import file_changes
from OpenDrive.client_side import file_changes_json
from OpenDrive.client_side import paths as client_paths
from OpenDrive.client_side import gui
from OpenDrive import net_interface
from OpenDrive.client_side import main

from tests.helper_all import h_client_routine, h_start_server_process, h_stop_server_process, h_create_empty
from tests.client_side.helper_client import h_register_dummy_user_device_client


def h_watch_dummy_folder(folder_name: str):
    abs_path = os.path.join(client_paths.LOCAL_CLIENT_DATA, folder_name)
    os.makedirs(abs_path, exist_ok=True)
    file_changes.add_folder(abs_path)


def h_add_dummy_server_folder(folder_name: str):
    net_interface.server.add_folder(folder_name)


@h_client_routine()
def simulate_explorer():
    h_create_empty(client_paths.normalize_path(client_paths.LOCAL_CLIENT_DATA, "folder1"))
    h_register_dummy_user_device_client()
    file_changes_json.init_file(empty=True)
    h_add_dummy_server_folder("folder1")
    h_add_dummy_server_folder("folder2")
    gui.main.main()


@h_client_routine(clear_folders=True)
def simulate_main():
    h_register_dummy_user_device_client()
    main_thread = threading.Thread(target=main.start, daemon=True)
    main_thread.start()
    gui.main.main()
    main.shutdown()


@h_client_routine(clear_server_db=True, clear_folders=True)
def simulate_register():
    file_changes_json.init_file()
    gui.main.main()


if __name__ == '__main__':
    server_process = h_start_server_process()
    simulate_register()
    h_stop_server_process(server_process)
