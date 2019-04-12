"""
:module: OpenDrive.server_side.authentication
:synopsis: Functions, to authenticate, login, register a user/device
:author: Julian Sobott
    
public functions
-----------------

.. autofunction:: register_user_device

.. autofunction:: login_manual_user_device

.. autofunction:: login_auto

private functions
------------------

.. autofunction:: _add_update_device

.. autofunction:: _set_user_authenticated

"""
import pynetworking as net
from passlib.apps import custom_app_context as pwd_context
from typing import Optional, Tuple, Union

from OpenDrive.server_side.database import User, Device, DeviceUser, Token
from OpenDrive.server_side.od_logging import logger
from OpenDrive.server_side import folders


def register_user_device(username: str, password: str, mac_address: str, email: Optional[str] = None) -> \
        Union[str, Token]:
    """Registers a new user and adds the device to the db if it is not already in the db. On success a Token is
    returned. This Token is used for auto-login. On any failure a string with the error message is returned."""
    assert len(username) > 3, "Username must be at least 4 characters long!"
    assert len(password) > 4, "Password must be at least 5 characters long!"

    possible_user = User.get_by_username(username)
    if possible_user is not None:
        return "Username is already taken"
    hashed_password = pwd_context.hash(password)
    user_id = User.create(username, hashed_password, email)
    token, device_id = _add_update_device(mac_address)
    DeviceUser.create(device_id, user_id)
    _set_user_authenticated()
    folders.create_folder_for_new_user(User.from_id(user_id))
    return token


def login_manual_user_device(username: str, password: str, mac_address: str) -> Union[str, Token]:
    """Try to login by username and password. A token for auto-login is returned"""
    possible_user = User.get_by_username(username)
    if possible_user is None:
        return f"No user with username: {username}."
    user = possible_user
    if not pwd_context.verify(password, user.password):
        return "Entered wrong password."
    device_exist = Device.get_by_mac(mac_address) is not None
    token, device_id = _add_update_device(mac_address)
    if not device_exist:
        DeviceUser.create(device_id, user.id)
    _set_user_authenticated()
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
    _set_user_authenticated()
    return True


def logout() -> None:
    _set_user_authenticated(False)


def _add_update_device(mac_address: str) -> Tuple[Token, int]:
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
    device_id = Device.create(mac_address, Token(), Token.get_next_expired())
    device_token = Device.from_id(device_id).token
    return device_token, device_id


def _set_user_authenticated(value: bool = True) -> None:
    """Set the client, to be authenticated. This allows further communication."""
    client = net.ClientManager().get()
    client.is_authenticated = value
