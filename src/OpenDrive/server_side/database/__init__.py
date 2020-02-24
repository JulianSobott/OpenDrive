"""
:module: OpenDrive.server_side.database
:synopsis: DB access at the server-side
:author: Julian Sobott

Tables
-------

- users (user data)
- folders (Server paths, user (for path)? )
- changes (files changed. folder. device)
- privileges (folder, user, privileges)
- devices (device_id, user_id, mac_address, token)

- sync_folders (client_folder, server_folder, device_user)

Modules
--------

.. automodule:: OpenDrive.server_side.database.devices
.. automodule:: OpenDrive.server_side.database.folders
.. automodule:: OpenDrive.server_side.database.general
.. automodule:: OpenDrive.server_side.database.users
"""
from OpenDrive.server_side.database.general import create_database, DBConnection
from OpenDrive.server_side.database.users import User
from OpenDrive.server_side.database.devices import Device
from general.database import Token
from OpenDrive.server_side.database.folders import Folder

