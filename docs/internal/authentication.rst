Authentication
=================

After establishing a stable connection with the server (managed by the pynetworking library) the device needs to be
authenticated. File changes are tracked always even when the device is offline or the authentication fails.
A synchronization between client and server only starts, when the device is authenticated.

Authentication options
--------------------------

Registration
^^^^^^^^^^^^^^^^

- The user enters username, password and optional email(mac_address) and sends it to the server.
- The server checks if the username is already used: returns an error if so
- The server hashes the password
- The server inserts the data into the table
- Create a new user_device entry
- Create a new device entry with a generated token: return the token

Login (Manual)
^^^^^^^^^^^^^^^^

- The user enters username, password, mac_address is read and sends it to the server
- The Server selects the username: if not found return error
- The server checks if the password is valid: if not return fail
- The server checks if mac is in devices
- If mac in devices: generate a new token and return it with success
- If not insert a new entry
- Generate a new token and return it

Login (Auto)
^^^^^^^^^^^^^^^^

- The client reads the stored token, unique device data and sends it to the server
- The server checks data: on success login and returns success

API
----

Client
^^^^^^^^^^

.. automodule:: OpenDrive.client_side.authentication

Server
^^^^^^^^^^

.. automodule:: OpenDrive.server_side.authentication