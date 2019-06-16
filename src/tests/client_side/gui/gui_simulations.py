import threading
import time

from OpenDrive.client_side import file_changes_json
from OpenDrive.client_side import main as main_prog
from OpenDrive.client_side.gui import main
from OpenDrive.client_side.gui import screens
from tests.client_side.gui.test_explorer import h_watch_dummy_folder
from tests.client_side.helper_client import h_register_dummy_user_device_client
from tests.helper_all import h_client_routine, h_start_server_process, h_stop_server_process


def h_server_client(func):
    def wrapper(*args, **kwargs):
        @h_client_routine(clear_folders=True)
        def exe():
            return func(*args, **kwargs)

        server_process = h_start_server_process()
        ret = exe()
        h_stop_server_process(server_process)
        return ret
    return wrapper


@h_server_client
def start_from_zero():
    main.main(screens.REGISTRATION)


@h_server_client
def authentication_only():
    main.main(screens.REGISTRATION, authentication_only=True)


@h_server_client
def auto_login():
    """Gui auto login -> explorer"""
    h_register_dummy_user_device_client()
    file_changes_json.init_file(empty=True)
    time.sleep(1)

    main_thread = threading.Thread(target=main_prog.start, daemon=True)
    main_thread.start()

    time.sleep(2)
    #interface.add_sync_folder(c_paths.normalize_path(c_paths.LOCAL_DATA, "folder1"), "folder1")
    main.main(screens.REGISTRATION, try_auto_login=True)



@h_server_client
def demonstration_example():
    user = h_register_dummy_user_device_client()
    print(f"Username: {user.username}")
    print(f"Password: {user.password}")

    main_thread = threading.Thread(target=main_prog.start, daemon=True)
    main_thread.start()

    time.sleep(3)
    main.main(screens.LOGIN_MANUAL, try_auto_login=False)


@h_server_client
def simulate_many_folders():
    h_register_dummy_user_device_client()
    file_changes_json.init_file()
    for i in range(3):
        h_watch_dummy_folder(f"folder {i}")
        time.sleep(0.1)
    time.sleep(2)
    main.main(screens.REGISTRATION, try_auto_login=True)


if __name__ == '__main__':
    auto_login()
