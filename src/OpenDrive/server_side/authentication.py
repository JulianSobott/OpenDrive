"""
:module: OpenDrive.server_side.authentication
:synopsis: Functions, to authenticate, login, register a user/device
:author: Julian Sobott
    
public functions
-----------------

.. autofunction:: register_user_device

private functions
------------------

.. autofunction:: _add_update_device

"""
from passlib.apps import custom_app_context as pwd_context
from typing import Optional, Tuple, Union

from OpenDrive.server_side.database import User, Device, DeviceUser, Token
from OpenDrive.server_side.od_logging import logger


def register_user_device(username: str, password: str, mac_address: str, email: Optional[str] = None) -> \
        Union[str, Token]:
    """Registers a new user and adds the device to the db if it is not already in the db. On success a Token is
    returned. This Token is used for auto-login. On any failure a string with the error message is returned."""
    assert len(username) > 3, "Username must be at least 4 characters long!"
    assert len(password) > 4, "Password must be at least 5 characters long!"
    assert len(mac_address) == 14, "Mac address string must have length 14! ('str(uuid.getnode())')"

    possible_user = User.get_by_username(username)
    if possible_user is not None:
        return "Username is already taken"
    hashed_password = pwd_context.hash(password)
    user_id = User.create(username, hashed_password, email)
    token, device_id = _add_update_device(mac_address)
    DeviceUser.create(device_id, user_id)
    logger.debug(type(token))
    return token


def _add_update_device(mac_address: str) -> Tuple[Token, int]:
    """Adds a new device to the db. If the device already no device is added. A proper Token that isn't expired and
    the device_id is returned."""
    possible_device = Device.get_by_mac(mac_address)
    if possible_device is not None:
        if Token.is_token_expired(possible_device.token_expires):
            new_token = Token()
            possible_device.token = new_token
            possible_device.token_expires = Token.get_next_expired()
            return new_token, possible_device.device_id
        else:
            return possible_device.token, possible_device.device_id
    device_id = Device.create(mac_address, Token().token, Token.get_next_expired())
    device_token_string = Device.from_id(device_id).token
    return Token.from_string(device_token_string), device_id

