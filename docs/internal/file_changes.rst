File changes
============

One big advantage of OpenDrive is, that it synchronizes silently. So when a file is changed inside a synchronized folder
this is tracked. When the pc is connected to the server it then uploads the changes to the server. This works also when
a file change is marked at the server. Then the pc pulls the new changes.

Features
---------

- Track every change
- Recognize the following changes to a file and the necessary action on the other side:
    - Create  (File was not in any known previous location) -> Pull file
    - Move    (File was at a known location. Also rename)   -> Move file
    - Modify  (Files content changed)                       -> Pull file
    - Delete  (File is deleted and not at any new location) -> Delete file


- Store as much data as necessary to provide synchronisation with the other side, where it is clear what is the latest
  state of a file
- Only one entry per file, even when it changed multiple times

Considerations
---------------

Paths:
    - Use relative or absolute paths?
    - Paths relative to what?
    - depends also on the structure how changes are stored
        - Multiple changes in a folder could be stored memory efficient, when the path to the folder is only stored once


Details
--------

What data to store:
    - new_file_path
    - last_change_time_stamp
    - changes (Create, Move, Modify, Delete)
    - necessary_action (Pull, move, delete)
    - is directory
    - old_file_path (Only on move)


Store changes in a database.
There are two tables in the local database, that are responsible for file changes.
One stores all folders, to keep track of. The other stores all file changes. The second one has the folder_id as
foreign key. Some advantages are, that the folders, and the files can be stored in one db. No redundant paths can occur.
Easy to select changes in a specific folder.

**Database structure:** See: :doc:`client_database`.

The code, that is responsible for this task is located at `client_side/file_watcher.py`.

Implementation
--------------

1. For every folder there is a watcher that watches
2. On any change:
    - ignore? -> None
        - is already an entry? -> Change entry
            - add entry

Tests
---------

- get_entry(folder_id, rel_path) -> None, entry
