"""
:module: OpenDrive.server_side.authentication
:synopsis: Functions, to authenticate, login, register a user/device
:author: Julian Sobott
    
public functions
-----------------

.. autofunction:: login_auto
.. autofunction:: login_manual_user_device
.. autofunction:: logout
.. autofunction:: register_user
.. autofunction:: register_user_device

private functions
------------------

.. autofunction:: _add_update_device
.. autofunction:: _set_user_authenticated

"""
import os
import functools
import time

from passlib.apps import custom_app_context as pwd_context
from typing import Optional, Tuple, Union

from OpenDrive import net_interface
from OpenDrive.server_side.database import User, Device, Token
from OpenDrive.server_side.od_logging import client_logger_security
from OpenDrive.server_side import folders
from OpenDrive.server_side import paths as server_paths
from OpenDrive.server_side import file_changes_json as server_json


def register_user_device(username: str, password: str, mac_address: str, email: Optional[str] = None) -> \
        Union[str, Token]:
    """Registers a new user and adds the device to the db if it is not already in the db. On success a Token is
    returned. This Token is used for auto-login. On any failure a string with the error message is returned."""
    ret = register_user(username, password, email)
    if isinstance(ret, str):
        return ret
    else:
        user_id = ret
    token, device_id = _add_update_device(user_id, mac_address)
    client_logger_security().info(f"Successfully added new device: user_id={user_id}, device_id={device_id}")
    _set_user_authenticated(user_id, device_id)
    return token


def register_user(username: str, password: str, email: Optional[str] = None) -> Union[str, int]:
    """Registers a new user. On success the user_id  is returned. On any failure a string with the error message
    is returned. No device is added or registered."""
    fail_msg = ""
    if len(username) <= 3:
        fail_msg = "Username must be at least 4 characters long!"
    if len(password) <= 4:
        fail_msg = "Password must be at least 5 characters long!"
    possible_user = User.get_by_username(username)
    if possible_user is not None:
        fail_msg = "Username is already taken"
    if fail_msg:
        client_logger_security().info(f"Failed to register: {fail_msg}")
        return fail_msg
    else:
        hashed_password = pwd_context.hash(password)
        user_id = User.create(username, hashed_password, email)
        folders.create_folder_for_new_user(User.from_id(user_id))
        client_logger_security().info(f"Successfully registered user: user_id={user_id}")
        return user_id


def login_manual_user_device(username: str, password: str, mac_address: str) -> Union[str, Token]:
    """Try to login by username and password. A token for auto-login is returned"""
    possible_user = User.get_by_username(username)
    fail_msg = ""
    if possible_user is None:
        fail_msg = f"No user with username: {username}."
    user = possible_user
    if not pwd_context.verify(password, user.password):
        fail_msg = f"Wrong password"
    if fail_msg:
        client_logger_security().info(f"Failed to login manual: {fail_msg}")
        return "Wrong username or password"
    else:
        token, device_id = _add_update_device(user.id, mac_address)
        _set_user_authenticated(user.id, device_id)
        client_logger_security().info(f"Successfully logged in manual: device_id={device_id}, user_id={user.user_id}, "
                                      f"token={token}")
        return token


def login_auto(token: Token, mac_address: str) -> bool:
    """Login by the token and mac_address. Returns, whether it was successful or not."""
    device = Device.get_by_mac(mac_address)
    fail_msg = ""
    if device is None:
        fail_msg = "No device with mac address exist"
    if Token.is_token_expired(device.token_expires):
        fail_msg = "Token is expired"
    if token != device.token:
        fail_msg = "Wrong token"
    if fail_msg:
        client_logger_security().info(f"Failed to login automatically: {fail_msg}")
        return False
    else:
        _set_user_authenticated(device.user_id, device.device_id)
        client_logger_security().info(f"Successfully logged in automatically:  device_id={device.device_id}, "
                                      f"user_id={device.user_id}")
        return True


def logout() -> None:
    _set_user_authenticated(-1, -1, False)
    client_logger_security().info("Successfully logged out")
    # TODO: remove client from ClientManager


def _add_update_device(user_id: int, mac_address: str) -> Tuple[Token, int]:
    """Adds a new device to the db. If the device already exists no device is added. A proper Token that isn't
    expired and the device_id is returned."""
    possible_device = Device.get_by_mac(mac_address)
    if possible_device is not None:
        if Token.is_token_expired(possible_device.token_expires):
            new_token = Token()
            possible_device.token = new_token
            possible_device.token_expires = Token.get_next_expired()
            return new_token, possible_device.device_id
        else:
            return possible_device.token, possible_device.device_id
    device_id = Device.create(user_id, mac_address, Token(), Token.get_next_expired())
    device_token = Device.from_id(device_id).token
    assert os.path.exists(server_paths.get_users_root_folder(user_id))
    server_json.create_changes_file_for_new_device(user_id, device_id, empty=True)
    return device_token, device_id


def _set_user_authenticated(user_id: int, device_id: int, value: bool = True) -> None:
    """Set the client, to be authenticated. This allows further communication. Also stores the user_id."""
    client = net_interface.get_user()
    client.is_authenticated = value
    client.user_id = user_id
    client.device_id = device_id


def requires_authentication(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        user = net_interface.get_user()
        if not user.is_authenticated:
            client_logger_security().info(f"User is not authenticated to execute this function: "
                                          f"user={user}, function={func.__name__}")
        while not user.is_authenticated:
            # TODO: Maybe add max counter. Care to not crash the client program, because it expects a valid return
            net_interface.get_user().remote_functions.open_authentication_window()
            if not user.is_authenticated:
                client_logger_security().debug(f"User is still not authenticated! user={user}, "
                                               f"function={func.__name__}")
            time.sleep(1)  # TODO: add better way instead of sleep for create all files and setup all users stuff
        return func(*args, **kwargs)
    return wrapper

