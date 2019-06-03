from OpenDrive.client_side.gui import main
from OpenDrive.client_side.gui import screens

from tests.helper_all import h_client_routine, h_start_server_process, h_stop_server_process, h_create_empty
from tests.client_side.helper_client import h_register_dummy_user_device_client


@h_client_routine()
def start_from_zero():
    main.main(screens.REGISTRATION, authentication_only=True)


if __name__ == '__main__':
    server_process = h_start_server_process()
    start_from_zero()
    h_stop_server_process(server_process)