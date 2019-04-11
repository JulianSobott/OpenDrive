"""
:module: OpenDrive.client_side.authentication
:synopsis: Functions, to authenticate, login, register a user/device, with CLI
:author: Julian Sobott

public classes
---------------

.. autoclass:: XXX
    :members:
    
public functions
-----------------

.. autofunction:: XXX

private classes
----------------

private functions
------------------

"""
import getpass
from typing import Optional

from OpenDrive import net_interface
from OpenDrive.general.device_data import get_mac
from OpenDrive.server_side.database import Token
from OpenDrive.client_side import paths
from OpenDrive.client_side.od_logging import logger
from OpenDrive.net_interface import server


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
        mac_address = get_mac()
        ret = server.register_user_device(username, password, mac_address, email)
        if isinstance(ret, str):
            print(ret)
        else:
            print("Successfully registered")
            _save_received_token(ret)
            break


def login_manual_user_device_cli() -> None:
    if not net_interface.ServerCommunicator.is_connected():
        print("Can not connect to server. PLease try again later")
        return
    while True:
        username = input("Username: ")
        password = getpass.getpass("Password: ")
        mac_address = get_mac()
        ret = server.login_manual_user_device(username, password, mac_address)
        if isinstance(ret, str):
            print(ret)
        else:
            print("Successfully logged in")
            _save_received_token(ret)
            break


def login_auto() -> None:
    token = _get_token()
    if token is not None:
        mac = get_mac()
        success = server.login_auto(token, mac)
        if not success:
            login_manual_user_device_cli()
        else:
            logger.info("Successfully auto logged in")
    else:
        login_manual_user_device_cli()


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
