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

