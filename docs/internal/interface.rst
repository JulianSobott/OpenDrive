Interface
=============

Here are all functions defined, that are needed at the gui/ui.

- Login auto ()
- Login (username, password, [stay_logged_in])
- Logout ()
- Register (username, password, [email])
- Add folder (local_path, remote_name=local_path[1], [options?])
- Remove synchronization (local_path)
- Remove remote folder (remote_name)
- Share folder (username, permissions, remote_name)
- Get all remote folders ()
- Get all synced folder pairs
- Add ignore patterns to folder (patterns, local_path)
- [Force sync([local_folder])]
- [Solve merge conflicts()]
- [Create remote folder(remote_name)]

Code doc
^^^^^^^^^^

.. automodule:: OpenDrive.client_side.interface