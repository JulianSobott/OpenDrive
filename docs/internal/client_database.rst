=======================
Client database
=======================

Ad the client side there is one database used.

It has the following tables:
    - sync_folders
    - changes
    - ignores

The local_data.db file is located at *OpenDrive/local/client_side/local_data.db*.

Implementation
===============


At the source client_side the file *database.py* is responsible for the core features of the local database.

**Features**
    - Creating the database, with its tables
    - Making requests

As database_manager the sqlite3 module is used. It is available in the standard library.

**Database structure:**

*sync_folders*

    - folder_id
    - path

*changes* (Not 'files', because also it also tracks folders)

    - change_id
    - folder_id
    - current_rel_path (to folder)
    - is_folder
    - last_change_time_stamp
    - Create
    - Move
    - Modify
    - Delete
    - necessary_action (Pull, move, delete)
    - old_abs_path (Only on move)

*ignores* (All patterns that should be ignored and not synchronized (like .gitignore))

    - ignore_id
    - folder_id
    - pattern
    - sub_folders