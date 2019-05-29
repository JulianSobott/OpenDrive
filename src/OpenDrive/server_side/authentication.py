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

from passlib.apps import custom_app_context as pwd_context
from typing import Optional, Tuple, Union

from OpenDrive import net_interface
from OpenDrive.server_side.database import User, Device, Token
from OpenDrive.server_side.od_logging import logger
from OpenDrive.server_side import folders
from OpenDrive.server_side import paths as server_paths
from OpenDrive.server_side import file_changes_json as server_json


def register_user_device(username: str, password: str, mac_address: str, email: Optional[str] = None) -> \
        Union[str, Token]:
    """Registers a new user and adds the device to the db if it is not already in the db. On success a Token is
    returned. This Token is used for auto-login. On any failure a string with the error message is returned."""
    assert len(username) > 3, "Username must be at least 4 characters long!"
    assert len(password) > 4, "Password must be at least 5 characters long!"

    ret = register_user(username, password, email)
    if isinstance(ret, str):
        return ret
    else:
        user_id = ret
    token, device_id = _add_update_device(user_id, mac_address)
    _set_user_authenticated(user_id, device_id)
    return token


def register_user(username: str, password: str, email: Optional[str] = None) -> Union[str, int]:
    """Registers a new user. On success the user_id  is returned. On any failure a string with the error message
    is returned. No device is added or registered."""
    assert len(username) > 3, "Username must be at least 4 characters long!"
    assert len(password) > 4, "Password must be at least 5 characters long!"

    possible_user = User.get_by_username(username)
    if possible_user is not None:
        return "Username is already taken"
    hashed_password = pwd_context.hash(password)
    user_id = User.create(username, hashed_password, email)
    folders.create_folder_for_new_user(User.from_id(user_id))
    return user_id


def login_manual_user_device(username: str, password: str, mac_address: str) -> Union[str, Token]:
    """Try to login by username and password. A token for auto-login is returned"""
    possible_user = User.get_by_username(username)
    if possible_user is None:
        return f"No user with username: {username}."
    user = possible_user
    if not pwd_context.verify(password, user.password):
        return "Entered wrong password."
    token, device_id = _add_update_device(user.id, mac_address)
    _set_user_authenticated(user.id, device_id)
    return token


def login_auto(token: Token, mac_address: str) -> bool:
    """Login by the token and mac_address. Returns, whether it was successful or not."""
    device = Device.get_by_mac(mac_address)
    if device is None:
        return False
    if Token.is_token_expired(device.token_expires):
        return False
    if token != device.token:
        return False
    _set_user_authenticated(device.user_id, device.device_id)
    return True


def logout() -> None:
    _set_user_authenticated(-1, -1, False)
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
            user.remote_functions.open_gui_authentication()
            if not user.is_authenticated:
                return
        return func(*args, **kwargs)
    return wrapper
