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


Storing folder information
*****************************

All synchronized folders are stored inside a DB table. Any additional meta data can be added here later on:

    - folder_id
    - user_id (owner -> necessary for path)
    - folder_name

In Addition every folder that is synced with a device is stored in the accordingly changes.json file. This is needed to
assign changes to the appropriate folder.



Code docs
**********

.. automodule:: OpenDrive.server_side.folders

