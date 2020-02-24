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


- Store as much data as necessary to provide synchronization with the other side, where it is clear what is the latest
  state of a file
- Only one entry per file, even when it changed multiple times


Special cases
--------------

Nested folders
^^^^^^^^^^^^^^^^

It is NOT possible to nest folders.

- No use case
- Redundant files
- Harder to implement

But it is possible to add specific exclude include rules for subfolders, because of the power of regex. So instead
of adding a new folder with new rules, add new regex rules that only apply inside this folder. e.g. "inner/.*\.txt".
In the GUI this may be shown as it were a special rule for the subfolder.


File move
^^^^^^^^^^

For now, it only tracks, when a file is renamed and stays inside the same folder. If the file or folder is moved, to
another folder, it is recognized as `delete` at the old path and `create` at the new path. The disadvantage is,
that files, that probably already exist are deleted and then pulled again. To solve this enhancement is a possible
enhancement.

Implementation
--------------

1. For every folder, there is a watcher that watches
2. On any change:
    - ignore? -> None
        - is already an entry? -> Change entry
            - add entry


API
----

.. automodule:: OpenDrive.client_side.file_changes