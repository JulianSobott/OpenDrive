"""
:module: OpenDrive.server_side.authentication
:synopsis: Functions, to authenticate, login, register a user/device
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
from passlib.apps import custom_app_context as pwd_context
from typing import Optional, Tuple, Union

from OpenDrive.server_side.database import User, Device, DeviceUser, Token


def register_user_device(username: str, password: str, mac_address: str, email: Optional[str] = None) -> \
        Union[str, Token]:

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
    return token


def _add_update_device(mac_address: str) -> Tuple[Token, int]:
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

