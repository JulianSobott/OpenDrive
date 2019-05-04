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

API
-----

- start() -> watching at all specified folders
- add_folder() -> Check is folder possible, insert in json, start watching
- remove_folder -> remove from json, Stop watching (changes are deleted too)
- get_all_folders() -> return list of all folders
- add_single_ignores() -> ignore pulled files
- set_include_regexes()
- set_exclude_regexes()
- get_include_regexes()?
- get_exclude_regexes()?


Details
--------

What data to store:
    - new_file_path
    - last_change_time_stamp
    - changes (Create, Move, Modify, Delete)
    - necessary_action (Pull, move, delete)
    - is directory
    - old_file_path (Only on move)

What folders are watched and the changes are stored in one single json file.

**Json structure: changes.json**

File:
    Dict[folder_path: Folder]
Folder:
    server_folder_path: str
    include_regexes: List[str],
    exclude_regexes: List[str],
    changes: Dict[actual_file_path: Change]
Change:
    new_file_path: str,     # relative to folder_path (actual_file_path)
    last_change_time_stamp: int,
    changes: List[str], # move, delete, create, modify
    necessary_action: str, # pull, move, delete
    is directory: bool,
    ~old_file_path: str # Only on move in same folder, relative to folder_path


The code, that is responsible for this task is located at `client_side/file_changes.py`.

**Subfolders:**

It is NOT possible to nest folders.

- No use case
- Redundant files
- Harder to implement

But it is possible to add specific exclude include rules for subfolders, because of the power of regex. So instead
of adding a new folder with new rules, add new regex rules that only apply inside this folder. e.g. "inner/.*\.txt".
In the gui this may be shown as it where a special rule for the subfolder.



Implementation
--------------

1. For every folder there is a watcher that watches
2. On any change:
    - ignore? -> None
        - is already an entry? -> Change entry
            - add entry

Special case: `move`
*********************

The `create`, `delete` and `modified` changes are easy to track and implement. The `move event` is trickier. For
now it only tracks, when a file is renamed and stays inside the same folder. If the file or folder is moved, to another
folder, it is recognized as `delete` at the old path and `create` at the new path. The disadvantage is, that files, that
probably already exist are deleted and then pulled again. To solve this enhancement is a possible enhancement.

At Server:
---------------

Every user has its own root folder. Every root folder has one changes file for every device, that is associated with
this user. Every time a synchronization between a device and the server happens, these changes are written to all
other changes files. Only when these devices are synchronized with the folder. All changes file store the
server-folders which are synchronized.

The client must store the names/paths of the server folders. Which client folder is synced to which server folder. If
a server folders name is updated, this must be first translated to the client, and it must update all references.
Folder renames must also be stored in the changes file. TODO: how to store (root)-folder renames, delete??


Code doc
==========

.. automodule:: OpenDrive.client_side.file_watcher