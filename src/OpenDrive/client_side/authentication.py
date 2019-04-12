"""
:module: OpenDrive.client_side.authentication
:synopsis: Functions, to authenticate, login, register a user/device, with CLI
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

from OpenDrive import net_interface
from OpenDrive.general.device_data import get_mac
from OpenDrive.server_side.database import Token
from OpenDrive.client_side import paths
from OpenDrive.client_side.od_logging import logger
from OpenDrive.net_interface import server
from OpenDrive.client_side.interface import Status


def register_user_device(username: str, password: str, email: str = None) -> Status:
    mac_address = get_mac()
    ret = server.register_user_device(username, password, mac_address, email)
    if isinstance(ret, str):
        return Status.fail(ret)
    else:
        _save_received_token(ret)
        return Status.success("Successfully registered")


def login_manual(username: str, password: str, allow_auto_login=True) -> Status:
    if not net_interface.ServerCommunicator.is_connected():
        print("Can not connect to server. Please try again later")
        return Status.fail("Can not connect to server. Please try again later.")
    mac_address = get_mac()
    ret = server.login_manual_user_device(username, password, mac_address)
    if isinstance(ret, str):
        return Status.fail(ret)
    else:
        print("Successfully logged in")
        if allow_auto_login:
            _save_received_token(ret)
        return Status.success("Successfully logged in")


def logout():
    server.logout()
    net_interface.ServerCommunicator.close_connection()
    return Status.success("Successfully logged out.")


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


def register_user_device_cli() -> None:
    if not net_interface.ServerCommunicator.is_connected():
        print("Can not connect to server. PLease try again later")
        return
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
            break
        else:
            print(status.get_text())


def login_manual_user_device_cli() -> None:
    if not net_interface.ServerCommunicator.is_connected():
        print("Can not connect to server. PLease try again later")
        return
    while True:
        username = input("Username: ")
        password = getpass.getpass("Password: ")
        status = login_manual(username, password)
        print(status.get_text())
        if status.was_successful():
            break


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
