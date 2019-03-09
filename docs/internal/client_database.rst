=======================
Client database
=======================

Ad the client side there is one database used.

It has the following tables:
    - sync_folders
    - changes

The local_data.db file is located at *OpenDrive/local/client_side/local_data.db*.

Implementation
===============


At the source client_side the file *database.py* is responsible for the core features of the local database.

**Features**
    - Creating the database
    - Creating the tables
    - Making requests

As database_manager the sqlite3 module is used. It is available in the standard library.