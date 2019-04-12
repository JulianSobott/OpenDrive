Synchronize folders
====================

It is possible to synchronize a folder at the client side with a folder at the server side.

The folder names can be different. Only the content is synchronized.

Folder Structure at the server
*******************************

::

    root
    |
    |___user_{user_id}
    |   |
    |   |___folder_XYZ
    |   |
    |   |___folder_ZXY
    |
    |___user_{user_id}
    |   |
    |   |___folder_XYZ
    |   |
    |   |___folder_ZXY


Database at server
*******************

All synchronized folders are stored inside a DB table:

    - folder_id
    - user_id (owner -> necessary for path)
    - folder_name


Considerations
***************

Is it possible to nest synchronized folders.

e.g. S_A synced with C_A and S_A/S_B synced with C_D.

**Advantages:**

- More user friendly
    - The user may sync one upper folder at the one device, but one inner folder at another device

**Disadvantages:**


**Difficulties:**

- Doubled changes must be prevented
- Prevent one device to sync with inner folders
- Allow only for different devices
- Prevent deleting inner folder, that is synced with other device



Code docs
**********

.. automodule:: OpenDrive.server_side.folders

