from OpenDrive.client_side.gui import main
from OpenDrive.client_side.gui import screens

from tests.helper_all import h_client_routine, h_start_server_process, h_stop_server_process, h_create_empty
from tests.client_side.helper_client import h_register_dummy_user_device_client


def h_server_client(func):
    def wrapper(*args, **kwargs):
        @h_client_routine()
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
    main.main(screens.REGISTRATION, authentication_only=True, try_auto_login=True)


if __name__ == '__main__':
    authentication_only()
