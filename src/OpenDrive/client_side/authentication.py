"""
:module: OpenDrive.client_side.authentication
:synopsis: Functions, to authenticate, login, register a user/device.
:author: Julian Sobott


public functions
-----------------

.. autofunction:: login_auto
.. autofunction:: login_manual
.. autofunction:: login_manual_user_device_cli
.. autofunction:: logout
.. autofunction:: register_user_device
.. autofunction:: register_user_device_cli


private functions
------------------

.. autofunction:: _get_token
.. autofunction:: _save_received_token

"""
import getpass
from typing import Optional
import functools

from OpenDrive import net_interface
from OpenDrive.net_interface import server
from OpenDrive.general.device_data import get_mac
from OpenDrive.server_side.database import Token
from OpenDrive.client_side import paths
from OpenDrive.client_side.od_logging import logger
from OpenDrive.client_side.interface import Status


def connection_needed(func):
    """Only execute function, when device is connected to the server."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if not net_interface.ServerCommunicator.is_connected():
            return Status.fail("Can not connect to server. Please try again later.")
        ret_value = func(*args, **kwargs)
        return ret_value
    return wrapper


@connection_needed
def register_user_device(username: str, password: str, email: str = None) -> Status:
    mac_address = get_mac()
    ret = server.register_user_device(username, password, mac_address, email)
    if isinstance(ret, str):
        return Status.fail(ret)
    else:
        _save_received_token(ret)
        return Status.success("Successfully registered")


@connection_needed
def login_manual(username: str, password: str, allow_auto_login=True) -> Status:
    mac_address = get_mac()
    ret = server.login_manual_user_device(username, password, mac_address)
    if isinstance(ret, str):
        return Status.fail(ret)
    else:
        print("Successfully logged in")
        if allow_auto_login:
            _save_received_token(ret)
        return Status.success("Successfully logged in")


@connection_needed
def logout() -> Status:
    server.logout()
    net_interface.ServerCommunicator.close_connection()
    return Status.success("Successfully logged out.")


@connection_needed
def login_auto() -> Status:
    token = _get_token()
    if token is not None:
        mac = get_mac()
        success = server.login_auto(token, mac)
        if not success:
            return Status.fail("Failed to automatically log in.")
        else:
            logger.info("Successfully auto logged in")
            return Status.success("Successfully auto logged in")

    else:
        return Status.fail("Failed to automatically log in.")


@connection_needed
def register_user_device_cli() -> Status:
    while True:
        username = input("Username: ")
        while True:
            password = getpass.getpass("Password: ")
            repeat_password = getpass.getpass("Enter Password again: ")
            if password == repeat_password:
                break
            else:
                print("Passwords are not equal. Please enter them again.")
        email = input("Email: [None] ")
        if email == "":
            email = None
        status = register_user_device(username, password, email)
        if status.was_successful():
            return Status.success("Successfully logged in")
        else:
            print(status.get_text())


@connection_needed
def login_manual_user_device_cli() -> Status:
    while True:
        username = input("Username: ")
        password = getpass.getpass("Password: ")
        status = login_manual(username, password)
        print(status.get_text())
        if status.was_successful():
            return Status.success("Successfully logged in")


def _save_received_token(token: Token) -> None:
    with open(paths.AUTHENTICATION_PATH, "w+") as file:
        file.write(token.token)


def _get_token() -> Optional[Token]:
    try:
        with open(paths.AUTHENTICATION_PATH, "r") as file:
            token = file.read().strip()
            return Token.from_string(token)
    except FileNotFoundError:
        return None
