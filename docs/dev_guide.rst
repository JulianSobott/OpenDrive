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
    - GUI: JavaFX?, PyQT?, Website?


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

**Top to bottom tasks:**


Workflow:
=========

    - Define General part
    - Create broad documentation
    - Create specific documentation
    - Define code (not implement)
    - Create tests for documentation
    - Implement code


Style-guide:
=============

This guide defines naming conventions:
    - *Package*: snake_case
    - *Python file*: snake_case
    - *Class*: CamelCase
    - *Function*: snake_case
    - *Variables*: snake_case
    - *rst file* snake_case

TODO next:
==========

On any change at the client side the server should be notified and a synchronization process should start.
Therefore a connection between server and client is necessary. The connection starts, when the client starts
and is online. A mechanism to test if it is only or in other words, if it *can connect to the server* is necessary.
How to connect: the device needs to identify itself and authenticate, that it is allowed to connect to the server.
There are several ways to achieve this. The user can choose which he/she want to choose.

1. The user has to enter his/her credentials

    - Necessary when the following fails
    - Not very user friendly
    - Very secure

2. Auto-login - login is stored in a file

    - The device logs in with multiple data, that is unique per device
    - Should be also very secure, but there are ways to crack?
    - Very user friendly
    - Default case

To login the user needs an existing account for auto login the device must be registered.
At manual login the the device may be registered (depends on the users choice). To create
an account the user needs to register.

- Low level Connection: Setup networking stuff
- Setup Console UI


The user/device is now successfully logged in. What actions are possible or rather important?

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

TODOS:

- setup tests in setup.py
- dev_guide



Team
*********

- Überlegen welche GUI features
    - Ablauf
