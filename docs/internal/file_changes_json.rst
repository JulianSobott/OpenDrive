Storing file changes
======================

Every change to a file/folder inside a tracked folder is stored in a `json` file. In this file are also all folders
listed, which are synchronized and therefore watched.

File structure
---------------

**Both sides**

The following data is necessary in all changes.json files. It is needed for proper synchronization.

- File:
    + Dict[folder_path: NormalizedPath, Folder]
        # folder_path: - abs_path at client
        #              - rel path at server (to users root)
- Folder:
    + changes: Dict[file_path: NormalizedPath, Change]
        # file_path: relative to folder. path, where the file is currently located at the server/device
- Change:
    + action: ActionType
    + timestamp: str
    + is_directory: bool
    + rel_old_file_path: Optional[NormalizedPath] # only on move. Key at other side for Change

- ActionType:
    + str[pull, move, delete]


**Client:**

Extra data at the client.

- Folder:
    + server_folder_path: NormalizedPath
    + include_regexes: List[str],
    + exclude_regexes: List[str],


**Server:**

Every user has its own root folder. Every root folder has one changes file for every device, that is associated with
this user. Every time synchronization between a device and the server happens, these changes are written to all
other changes files, when these devices are synchronized with the folder. All changes file store the
server-folders which are synchronized.


API
----

General
^^^^^^^^^^

.. automodule:: OpenDrive.general.file_changes_json

Client
^^^^^^^^^^

.. automodule:: OpenDrive.client_side.file_changes_json

Server
^^^^^^^^^^

.. automodule:: OpenDrive.server_side.file_changes_json



