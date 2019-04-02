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

from OpenDrive import net_interface
from OpenDrive.general.device_data import get_mac
from OpenDrive.server_side.database import Token

server = net_interface.ServerCommunicator.remote_functions


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
    mac = get_mac()
    success = server.login_auto(token, mac)
    if not success:
        login_manual_user_device_cli()


def _save_received_token(token: Token) -> None:
    print(token)


def _get_token() -> Token:
    pass
