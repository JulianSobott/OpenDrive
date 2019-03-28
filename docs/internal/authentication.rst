Authentication
=================

After establishing a stable connection with the server (managed by the networking library) the device needs to be
authenticated.File changes are tracked always even when the device is offline or the authentication fails.
The device needs to be authenticated. Options:

1. The user has to enter his/her credentials (username + password)

    - Necessary when the following fails
    - Not very user friendly
    - Very secure (weak passwords?)

2. Auto-login - login is stored in a file

    - The device logs in with multiple data, that is unique per device
    - Should be also very secure, but there are ways to crack?
    - Very user friendly
    - Default case

To login the user needs an existing account for auto login the device must be registered.
At manual login the the device may be registered (depends on the users choice). To create
an account the user needs to register.

Synchronization only starts, when the device is authenticated. This said it is not enough when the user is logged
in. The device data needs to be added/changed in the db and may be transmitted to the client. Only then the
synchronization process starts.


Process to start synchronization at device
-------------------------------------------

There are separate cases/functions for login/register on a website.

Suppose there is an existing connection to the server.

Registration
*************

- The user enters username, password and optional email(mac_address) and sends it to the server.
- The server checks if the username is already used: returns error if so
- The server hashes the password
- The server inserts the data into the table
- Create a new user_device entry
- Create a new device entry with a generated token: return the token

Login (Manual)
****************

- The user enters username, password, mac_address is read and sends it to the server
- The Server selects the username: if no found return error
- The server checks if password is valid: if not return fail
- The server checks if mac is in devices
- If mac in devices: generate new token and return it with success
- If not insert a new entry
- Generate a new token and return it

Login (Auto)
***************

- The client reads the stored token, unique device data and send it to the server
- Server checks data: on success login and return success
