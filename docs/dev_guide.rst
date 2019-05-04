==========
Dev Guide
==========

General
=================

**Abstract:**

Open Drive is an open source, self hosting alternative to GoogleDrive

**Problem:**

Many people need a kind of backup system and want data to be synchronized. They don't want their data to be stored at
servers in america or in general any third party.

**Solution:**

Use your own server and OpenDrive.

**Target Group:**

People with different devices. People with critical/important data. People who want to make a backup.


**Core functionality:**
    - Automatically sync your files between multiple devices
    - Define which file/folders to sync
    - No third parties have access to your data


**Possible features:**
    - Share your files and make them available for other people
    -  Access your files from everywhere, where you have internet access
    - Smartphone app


Details:
========

**Software:**
    - Core: python (with networking library)
    - GUI: JavaFX?, PyQT?, Website, Kivy?


**Project structure:**

::

    OpenDrive
    |   README.md
    |   setup.py
    |
    |___assets
    |       logo.png
    |
    |___docs
    |   |   index.rst
    |   |
    |   |____build
    |   |
    |   |___internal
    |   |
    |   |___external
    |
    |___src
    |   |
    |   |___OpenDrive
    |   |   |   debug_client_server.py
    |   |   |   net_interface.py
    |   |   |   start.py ?
    |   |   |
    |   |   |___client_side
    |   |   |
    |   |   |___server_side
    |   |   |
    |   |   |___general
    |   |
    |   |___tests
    |   |   |
    |   |   |___client_side
    |   |   |
    |   |   |___server_side
    |   |   |
    |   |   |___general


Workflow:
=========

One important point of this project is "clean" development process. The following list contains a possible workflow
(when a new feature is implemented), that can help to achieve this.

- Create broad documentation
- Create specific documentation
- Define code (not implement)
- Create tests for documentation
- Implement code
- Add code specific documentation

Style-guide:
=============

This guide defines naming conventions:

- *Package*: snake_case
- *Python file*: snake_case
- *Class*: CamelCase
- *Function*: snake_case
- *Variables*: snake_case
- *rst file* snake_case

Milestones
===========

- Exchange files based on actions: 26.04.19
- System for storing changes: 03.05.19
- Merge changes between server and client. Result in actions: 12.05.19
- Merge two existing folders. (Result in actions?): 19.05.19
- GUI Layouts: 25.05.19
- Connection between GUI and backend: 02.06.19
- (Installable)
- (Start on system start)

Tasks
=======

- GUI
    - Define features
    - Define procedure
    - Draft the gui design

- UI
    - Console interface
    - Same interface between console and gui

- Backend
    - folders
        - Add folder to be synchronized
            - local folder
            - server folder (existing one/create new)
        - Get all existing server folders
        - Remove folder synchronization
        - Remove server folder (danger)
        - Merge folders
            - Merge conflicts?
        - Edit folder privileges
            - Share link
            - Add user
            - Privileges
                - Edit
                - View
                - Full access (edit, view, delete)
    - Get files


TODO next:
==========

- GUI define features
- Implement Interface between backend, ui, gui
- Main program
    - startup                      <---
        - start watching
        - connect to server
            - success:
                - authenticate
                - get changes from server   <--- 2.
                - sync everything
    - main loop
        - sync on changes at the client
    - shutdown
        - is finished syncing?
        - close connection to server
        - stop watching

    - special cases
        - new folder added at client
            - mark everything as created?
        - existing client folder is merged with existing server folder
            - options:
                - use latest
                - use one side
                - decide individual
                - make copies of duplicates

- Store changes at server   <--- 1.
    -

