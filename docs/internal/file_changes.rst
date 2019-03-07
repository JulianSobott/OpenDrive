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

How to store changes?
    - local db
    - txt file with own formatting
    - json
    - csv

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
