TODOs in logging
----------------

- Add consistent logging
- Add fast option to log into file

Logger structure
################

[LEVEL] [TOPIC] MESSAGE [TIME] (CODE POSITION) (THREAD_NAME)


Client side
###########

General:
^^^^^^^^

- start tray    ✓
- start synchronization     ✓
- start connection to server    ✓
- open gui  ✓
    - manual/automatic  ✓
- stop program  ✓


Network:
^^^^^^^^

- Could not connect to server   (Not possible in OpenDrive)
    - Trying again every x seconds till y seconds   (Not possible in OpenDrive)
- Successfully connected to server (Address)     ✓
- Closed connection to server   ✓
- unexpectedly lost connection  (Not possible in OpenDrive)

Synchronization:
^^^^^^^^^^^^^^^^

- Watching at folders: folders_list
- Make general sync
- Receive files: files_list (compress/only folders if to much)
- Send files: files_list (compress/only folders if to much)


Server side
############

General
^^^^^^^

- Start server

Network
^^^^^^^^

- client connected
- client disconnected


Synchronization
^^^^^^^^^^^^^^^

(For each client an extra logger/file)

- Make general sync
- Receive files: files_list (compress/only folders if to much)
- Send files: files_list (compress/only folders if to much)

