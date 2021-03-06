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
    - Core: python (with pynetworking library)
    - GUI: python with Kivy, maybe later on a website?


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
    - input validation
    - beautiful design
    - TextInput without tabs (TF basic class)

(- UI
    - Console interface
    - Same interface between console and gui)

- Backend
    - folders
        - Remove folder synchronization
        - Remove server folder (danger)
        - implement all merge_methods
        - Edit folder privileges
            - Share link
            - Add user
            - Privileges
                - Edit
                - View
                - Full access (edit, view, delete)
    - synchronization
        - test: distribute actions to other changes files


TODO next:
==========

- Explorer:
    - validate patterns
    - process patterns
    - add sync with: paths, patterns and merge_method
    - hide merge_method, when a new server folder is created
    - option to delete server folder permanently

- test synchronization with multiple devices
